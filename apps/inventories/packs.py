from django.utils.translation import gettext_lazy as _

from faclab.base import BasePack
from viewpack.decorators import register

from .forms import ProductCategoryForm, ProductForm
from .formsets import ProductPriceFormset


@register("inventories.ProductCategory")
class ProductCategoryPack(BasePack):
    form_class = ProductCategoryForm
    list_fields = ("name", "parent")
    detail_fields = ("name", "parent")


@register("inventories.Measure")
class MeasurePack(BasePack):
    list_fields = ("code", "name")
    detail_fields = ("code", "name")


@register("inventories.Product")
class ProductPack(BasePack):
    form_class = ProductForm
    inlines = {"prices": ProductPriceFormset}
    form_template_name = None
    detail_template_name = None
    list_fields = ("code", "name", "short_name")
    detail_fields = {
        "": ProductForm.Meta.fieldsets,
        _("additional information"): ("type", "category", "measure"),
    }
