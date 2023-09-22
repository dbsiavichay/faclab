from django.utils.translation import gettext_lazy as _

from faclab.base import BasePack
from viewpack.decorators import register
from viewpack.enums import PackViews

from .forms import CustomerForm, InvoiceForm, InvoiceLineFormset, InvoicePaymentFormset
from .tasks import sign_and_send_invoice_task


@register("sales.VoucherType")
class VoucherTypePack(BasePack):
    list_fields = ("code", "name", "current", "ends")


@register("sales.Customer")
class CustomerPack(BasePack):
    form_class = CustomerForm
    list_fields = ("code_type", "code", "bussiness_name")
    detail_fields = CustomerForm.Meta.fieldsets


@register("sales.Invoice")
class InvoicePack(BasePack):
    form_class = InvoiceForm
    allowed_views = (PackViews.LIST, PackViews.CREATE, PackViews.DETAIL)
    inlines = {"lines": InvoiceLineFormset, "payments": InvoicePaymentFormset}
    list_fields = (
        "customer",
        "number",
        "issue_date",
        "subtotal",
        "tax",
        "total",
        "status",
    )
    detail_fields = (("customer", "issue_date"), ("code", "authorization_date"))
    form_template_name = None
    detail_template_name = None

    default_labels = {"number": _("number")}

    def post_save_inlines(self, instance):
        sign_and_send_invoice_task.apply_async(args=[instance.id])
