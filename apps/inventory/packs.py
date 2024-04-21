from django.utils.translation import gettext_lazy as _

from faclab.base import BasePack
from viewpack.decorators import register
from viewpack.enums import PackViews

from .infra.forms import ProductCategoryForm, ProductForm, ProviderForm, PurchaseForm
from .infra.formsets import ProductPriceFormset, PurchaseLineFormset


@register("inventory.Provider")
class ProviderPack(BasePack):
    form_class = ProviderForm
    list_fields = ("code", "bussiness_name", "contact_name")
    detail_fields = ProviderForm.Meta.fieldsets


@register("inventory.ProductCategory")
class ProductCategoryPack(BasePack):
    form_class = ProductCategoryForm
    list_fields = ("name", "parent")
    detail_fields = ("name", "parent")


@register("inventory.Measure")
class MeasurePack(BasePack):
    list_fields = ("code", "name")
    detail_fields = ("code", "name")


@register("inventory.Product")
class ProductPack(BasePack):
    form_class = ProductForm
    inlines = {"prices": ProductPriceFormset}
    form_template_name = None
    detail_template_name = None
    list_fields = ("code", "name", "short_name")
    detail_fields = {
        "": ProductForm.Meta.fieldsets,
        _("additional information"): (
            "type",
            "provider",
            "category",
            "measure",
            "warehouse_location",
        ),
    }


@register("inventory.Purchase")
class PurchasePack(BasePack):
    form_class = PurchaseForm
    allowed_views = (
        PackViews.LIST,
        PackViews.CREATE,
        PackViews.DELETE,
        PackViews.DETAIL,
    )
    inlines = {"lines": PurchaseLineFormset}
    list_fields = (
        "provider",
        "invoice_number",
        "subtotal",
        "tax",
        "total",
    )
    detail_fields = ("provider", ("date", "invoice_number"))
    form_template_name = None
    detail_template_name = None
