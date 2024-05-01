from faclab.base import BasePack
from viewpack.decorators import register
from viewpack.enums import PackViews

from .infra.forms import PurchaseForm
from .infra.formsets import PurchaseLineFormset


@register("purchase.Purchase")
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
