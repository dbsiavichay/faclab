from django import forms
from django.utils.translation import gettext_lazy as _

from faclab.base import PercentInput, PriceInput
from viewpack.forms import ModelForm

from .enums import PriceTypes
from .models import Price, Product


class ProductForm(ModelForm):
    cost_price = forms.FloatField(widget=PriceInput, label=_("price net"))
    cost_price_gross = forms.FloatField(widget=PriceInput, label=_("price gross"))

    class Meta:
        model = Product
        fieldsets = (
            "code",
            "name",
            "short_name",
            "description",
            ("is_inventoried", "apply_iva", "apply_ice"),
        )
        fields = ("cost_price", "cost_price_gross", "type", "category", "measure")
        widgets = {"type": forms.RadioSelect}

    def get_initial_for_field(self, field, field_name):
        if field_name in ("cost_price", "cost_price_gross"):
            return getattr(self.instance, field_name, None)

        return super().get_initial_for_field(field, field_name)

    def save(self, commit=True):
        obj = super().save(commit=False)

        if commit:
            obj.save()
            price = obj.prices.filter(type=PriceTypes.PURCHASE).first()
            cost_price = self.cleaned_data.get("cost_price")

            if price:
                price.amount = cost_price
                price.save(update_fields=["amount"])
            else:
                Price.objects.create(
                    type=PriceTypes.PURCHASE, amount=cost_price, revenue=0, product=obj
                )

        return obj


class PriceForm(ModelForm):
    gross_amount = forms.FloatField(widget=PriceInput, label=_("price gross"))
    percent_revenue = forms.FloatField(
        min_value=0, max_value=100, widget=PercentInput, label=_("percent revenue")
    )

    class Meta:
        model = Price
        fields = ("amount", "gross_amount", "percent_revenue", "revenue")
        labels = {"amount": _("price net")}
        widgets = {"amount": PriceInput, "revenue": PriceInput}

    def get_initial_for_field(self, field, field_name):
        if field_name in ("gross_amount", "percent_revenue"):
            return getattr(self.instance, field_name, None)

        return super().get_initial_for_field(field, field_name)

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.type = PriceTypes.SALE

        if commit:
            obj.save()

        return obj
