from dependency_injector.wiring import Provide, inject
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.core.application.services import SiteService
from apps.inventories.querysets import ProductQueryset
from faclab.widgets import DisabledNumberInput, PriceInput, Select2
from viewpack.forms import ModelForm

from .models import Customer, Invoice, InvoiceLine, InvoicePayment
from .services import InvoiceService
from .validators import customer_code_validator


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
        site_service: SiteService = Provide["core_package.site_service"],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.site_service = site_service

    class Meta:
        model = Invoice
        fieldsets = ("customer",)
        widgets = {
            "customer": Select2(
                model="sales.Customer",
                search_fields=[
                    "code__icontains",
                    "first_name__icontains",
                    "last_name__icontains",
                ],
            )
        }

    def save(self, commit=True):
        config = self.site_service.get_sri_config()
        obj = super().save(commit=False)
        obj.company_code = config.company_code
        obj.company_point_sale_code = config.company_point_sale_code

        if not obj.sequence:
            InvoiceService.generate_sequence(obj, commit=False)

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

    def save(self, commit=True):
        obj = super().save(commit=False)
        InvoiceService.calculate_line_totals(obj)

        if commit:
            obj.save()

        return obj


class InvoiceLineInlineFormset(forms.BaseInlineFormSet):
    def save(self, commit=True):
        object_list = super().save(commit=commit)
        InvoiceService.generate_access_code(self.instance, commit=False)
        InvoiceService.calculate_totals(self.instance, commit=False)
        self.instance.save()

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
