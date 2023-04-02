from faclab.base import BasePack
from viewpack.decorators import register

from .forms import ProductForm


@register("warehouses.ProductCategory")
class ProductCategoryPack(BasePack):
    list_fields = ("name", "parent")
    detail_fields = ("name", "parent")


@register("warehouses.Measure")
class MeasurePack(BasePack):
    list_fields = ("code", "name")
    detail_fields = ("code", "name")


@register("warehouses.Product")
class ProductPack(BasePack):
    form_class = ProductForm
    form_template_name = None
    list_fields = ("code", "name", "short_name")
    detail_fields = (
        "code",
        "name",
        "short_name",
        "description",
        "is_inventoried",
        "apply_iva",
        "apply_ice",
        "type",
        "category",
        "measure",
    )