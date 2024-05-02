from django import forms

from apps.inventory.domain.choices import PriceType

from .forms import ProductPriceForm
from .models import Product, ProductPrice


class ProductPriceInlineFormset(forms.BaseInlineFormSet):
    def get_queryset(self):
        return super().get_queryset().filter(type=PriceType.SALE)


ProductPriceFormset = forms.inlineformset_factory(
    Product,
    ProductPrice,
    form=ProductPriceForm,
    formset=ProductPriceInlineFormset,
    extra=1,
)
