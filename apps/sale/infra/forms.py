from dependency_injector.wiring import Provide, inject
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.core.domain.repositories import SiteRepository
from apps.inventory.infra.querysets import ProductQueryset
from apps.sale.application.services import InvoiceService
from apps.sale.application.validators import customer_code_validator
from apps.sale.domain.entities import InvoiceEntity, InvoiceLineEntity
from faclab.widgets import DisabledNumberInput, PriceInput, Select2
from viewpack.forms import ModelForm

from .models import Customer, Invoice, InvoiceLine


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
