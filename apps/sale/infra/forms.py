import pytz
from dependency_injector.wiring import Provide, inject
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.core.domain.repositories import SiteRepository
from apps.inventories.querysets import ProductQueryset
from apps.sale.application.services import InvoiceService
from apps.sale.application.validators import customer_code_validator
from apps.sale.domain.entities import CustomerEntity, InvoiceEntity, InvoiceLineEntity
from apps.sale.infra.tasks import send_invoice_task
from apps.sale.models import Customer, Invoice, InvoiceLine, InvoicePayment
from faclab.widgets import DisabledNumberInput, PriceInput, Select2
from viewpack.forms import ModelForm


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fieldsets = (
            ("code_type", "code"),
            ("first_name", "last_name"),
            "bussiness_name",
            "address",
            ("phone", "email"),
        )

    def clean(self):
        cleaned_data = super().clean()
        code_type = cleaned_data.get("code_type")
        code = cleaned_data.get("code")

        if code_type and code:
            long = len(code)

            if code_type.length != long:
                raise ValidationError(
                    _("The code entered does not correspond to a %(code_type)s"),
                    params={"code_type": code_type.name},
                )

            if code_type.code in ("04", "05"):
                customer_code_validator(code)

        return cleaned_data


class InvoiceForm(ModelForm):
    @inject
    def __init__(
        self,
        site_repository: SiteRepository = Provide["core_package.site_repository"],
        invoice_service: InvoiceService = Provide["sale_package.invoice_service"],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.site_repository = site_repository
        self.invoice_service = invoice_service

    class Meta:
        model = Invoice
        fieldsets = ("customer",)
        widgets = {
            "customer": Select2(
                model="sale.Customer",
                search_fields=[
                    "code__icontains",
                    "first_name__icontains",
                    "last_name__icontains",
                ],
            )
        }

    def save(self, commit=True):
        config = self.site_repository.get_sri_config()
        obj = super().save(commit=False)
        obj.voucher_type_code = "01"
        obj.company_branch_code = config.company_branch_code
        obj.company_sale_point_code = config.company_sale_point_code

        if not obj.sequence:
            invoice_entity = InvoiceEntity(**obj.__dict__)
            self.invoice_service.update_invoice_sequence(invoice_entity)
            obj.sequence = invoice_entity.sequence

        if commit:
            obj.save()

        return obj


class InvoiceLineForm(ModelForm):
    subtotal = forms.FloatField(
        widget=DisabledNumberInput, required=False, label=_("subtotal")
    )

    class Meta:
        model = InvoiceLine
        fields = ("product", "quantity", "unit_price", "subtotal")
        widgets = {
            "unit_price": PriceInput,
            "product": Select2(
                queryset=ProductQueryset.product_with_first_price,
                search_fields=["name__icontains"],
                extra_data=("first_price",),
            ),
        }

    @inject
    def __init__(
        self,
        invoice_service: InvoiceService = Provide["sale_package.invoice_service"],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.invoice_service = invoice_service

    def save(self, commit=True):
        obj = super().save(commit=False)

        invoiceline_entity = InvoiceLineEntity(**obj.__dict__)
        self.invoice_service.update_invoice_line_total(invoiceline_entity)
        obj.__dict__.update(
            invoiceline_entity.model_dump(include=["subtotal", "tax", "total"])
        )

        if commit:
            obj.save()

        return obj


class InvoiceLineInlineFormset(forms.BaseInlineFormSet):
    @inject
    def __init__(
        self,
        invoice_service: InvoiceService = Provide["sale_package.invoice_service"],
        *args,
        **kwargs
    ) -> None:
        self.invoice_service = invoice_service
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        object_list = super().save(commit=commit)
        timezone = pytz.timezone(settings.TIME_ZONE)
        customer = self.instance.customer
        customer_entity = CustomerEntity(
            code_type_code=customer.code_type.code, **self.instance.customer.__dict__
        )
        invoice_lines = [line.__dict__ for line in object_list]
        invoice_dict = {
            **self.instance.__dict__,
            "date": self.instance.date.astimezone(timezone),
        }
        invoice_entity = InvoiceEntity(
            customer=customer_entity, lines=invoice_lines, **invoice_dict
        )
        self.invoice_service.update_invoice_access_code(invoice_entity)
        self.invoice_service.update_invoice_total(invoice_entity)
        update_fields = ["access_code", "subtotal", "tax", "total"]
        self.instance.__dict__.update(invoice_entity.model_dump(include=update_fields))
        self.instance.save(update_fields=update_fields)
        self.invoice_service.update_invoice_xml(invoice_entity, update_on_db=True)
        self.invoice_service.sign_invoice_xml(invoice_entity, update_on_db=True)
        send_invoice_task.apply_async(args=[self.instance.id])

        return object_list


InvoiceLineFormset = forms.inlineformset_factory(
    Invoice,
    InvoiceLine,
    form=InvoiceLineForm,
    formset=InvoiceLineInlineFormset,
    extra=1,
    min_num=1,
    validate_min=True,
)

InvoicePaymentFormset = forms.inlineformset_factory(
    Invoice,
    InvoicePayment,
    fields=("type", "amount"),
    extra=1,
)
