from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.warehouses.querysets import ProductQueryset
from faclab.widgets import DisabledNumberInput, PriceInput, Select2
from viewpack.forms import ModelForm

from .models import Customer, Invoice, InvoiceLine
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
    class Meta:
        model = Invoice
        fieldsets = (("customer", "date"), "number")
        widgets = {
            "customer": Select2(
                model="sales.Customer", search_fields=["code__icontains"]
            )
        }


class InvoiceLineForm(ModelForm):
    subtotal = forms.FloatField(
        widget=DisabledNumberInput, required=False, label=_("subtotal")
    )

    class Meta:
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
        obj.subtotal = obj.unit_price * obj.quantity
        obj.tax = obj.subtotal * 0.12
        obj.total = obj.subtotal * 1.12

        if commit:
            obj.save()

        return obj


class InvoiceLineInlineFormset(forms.BaseInlineFormSet):
    def save(self, commit=True):
        object_list = super().save(commit=commit)
        InvoiceService.calculate_totals(self.instance)

        return object_list


InvoiceLineFormset = forms.inlineformset_factory(
    Invoice,
    InvoiceLine,
    form=InvoiceLineForm,
    formset=InvoiceLineInlineFormset,
    extra=1,
)
