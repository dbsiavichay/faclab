from django import forms
from django.utils.translation import gettext_lazy as _

from apps.inventory.domain.choices import PriceTypes
from faclab.widgets import PercentInput, PriceInput, Select2
from viewpack.forms import ModelForm

from .models import Product, ProductCategory, ProductPrice, Provider


class ProviderForm(ModelForm):
    class Meta:
        model = Provider
        fieldsets = (
            "code",
            ("bussiness_name", "contact_name"),
            "address",
            ("phone", "email", "website"),
        )


class ProductCategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = "__all__"
        widgets = {
            "parent": Select2(
                model="sale.ProductCategory",
                search_fields=["name__icontains"],
            )
        }


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
        fields = (
            "cost_price",
            "cost_price_gross",
            "type",
            "category",
            "measure",
            "provider",
            "warehouse_location",
        )
        widgets = {"type": forms.RadioSelect}

    def get_initial_for_field(self, field, field_name):
        if field_name == "cost_price":
            cost_price = getattr(self.instance, "cost_price", None)
            return cost_price.amount if cost_price else 0

        if field_name == "cost_price_gross":
            cost_price = getattr(self.instance, "cost_price", None)
            return cost_price.gross_amount if cost_price else 0

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
                ProductPrice.objects.create(
                    type=PriceTypes.PURCHASE, amount=cost_price, revenue=0, product=obj
                )

        return obj


class ProductPriceForm(ModelForm):
    gross_amount = forms.FloatField(widget=PriceInput, label=_("price gross"))
    percent_revenue = forms.FloatField(
        min_value=0, max_value=100, widget=PercentInput, label=_("percent revenue")
    )

    class Meta:
        model = ProductPrice
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
