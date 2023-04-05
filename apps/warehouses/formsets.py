from django import forms

from .enums import PriceTypes
from .forms import PriceForm
from .models import Price, Product


class ProductPriceInlineFormset(forms.BaseInlineFormSet):
    def get_queryset(self):
        return super().get_queryset().filter(type=PriceTypes.SALE)


ProductPriceFormset = forms.inlineformset_factory(
    Product, Price, form=PriceForm, formset=ProductPriceInlineFormset, extra=1
)
