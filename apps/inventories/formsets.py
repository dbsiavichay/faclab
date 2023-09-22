from django import forms

from .enums import PriceTypes
from .forms import ProductPriceForm
from .models import Product, ProductPrice


class ProductPriceInlineFormset(forms.BaseInlineFormSet):
    def get_queryset(self):
        return super().get_queryset().filter(type=PriceTypes.SALE)


ProductPriceFormset = forms.inlineformset_factory(
    Product,
    ProductPrice,
    form=ProductPriceForm,
    formset=ProductPriceInlineFormset,
    extra=1,
)
