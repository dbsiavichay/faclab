from django import forms

from apps.inventory.enums import PriceTypes
from apps.inventory.services import PurchaseService

from .forms import ProductPriceForm, PurchaseLineForm
from .models import Product, ProductPrice, Purchase, PurchaseLine


class ProductPriceInlineFormset(forms.BaseInlineFormSet):
    def get_queryset(self):
        return super().get_queryset().filter(type=PriceTypes.SALE)


class PurchaseLineInlineFormset(forms.BaseInlineFormSet):
    def save(self, commit=True):
        object_list = super().save(commit=commit)
        PurchaseService.calculate_totals(self.instance, commit=False)
        self.instance.save()

        return object_list


ProductPriceFormset = forms.inlineformset_factory(
    Product,
    ProductPrice,
    form=ProductPriceForm,
    formset=ProductPriceInlineFormset,
    extra=1,
)


PurchaseLineFormset = forms.inlineformset_factory(
    Purchase,
    PurchaseLine,
    form=PurchaseLineForm,
    formset=PurchaseLineInlineFormset,
    extra=1,
    # min_num=1,
    # validate_min=True,
)
