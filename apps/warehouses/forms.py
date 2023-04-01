from django import forms

from viewpack.forms import ModelForm

from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fieldsets = (
            "code",
            "name",
            "short_name",
            "description",
            "is_inventoried",
            "apply_iva",
            "apply_ice",
        )
        fields = ("type", "category", "measure")
        widgets = {"type": forms.RadioSelect}
