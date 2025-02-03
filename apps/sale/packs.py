from dependency_injector.wiring import Provide, inject
from django.utils.translation import gettext_lazy as _

from apps.sale.infra.tasks import send_invoice_task
from faclab.base import BasePack
from viewpack.decorators import register
from viewpack.enums import PackViews

from .application.services import InvoiceService
from .infra.forms import CustomerForm, InvoiceForm
from .infra.formsets import InvoiceLineFormset, InvoicePaymentFormset


@register("sale.VoucherType")
class VoucherTypePack(BasePack):
    list_fields = ("code", "name", "current", "ends")


@register("sale.Customer")
class CustomerPack(BasePack):
    form_class = CustomerForm
    list_fields = ("code_type", "code", "bussiness_name")
    detail_fields = CustomerForm.Meta.fieldsets


@register("sale.Invoice")
class InvoicePack(BasePack):
    form_class = InvoiceForm
    allowed_views = (PackViews.LIST, PackViews.CREATE, PackViews.DETAIL)
    inlines = {"lines": InvoiceLineFormset, "payments": InvoicePaymentFormset}
    list_fields = (
        "customer",
        "number",
        "date",
        "subtotal",
        "tax",
        "total",
        "status",
    )
    detail_fields = (("customer", "date"), ("access_code", "authorization_date"))
    form_template_name = None
    detail_template_name = None

    default_labels = {"number": _("number")}

    @inject
    def post_save_inlines(
        self,
        instance,
        invoice_service: InvoiceService = Provide["sale_package.invoice_service"],
    ):
        invoice_entity = invoice_service.build_invoice_entity(instance.id)
        invoice_service.update_invoice_xml(invoice_entity)
        invoice_service.seal_invoice_xml(invoice_entity, update_on_db=True)
        send_invoice_task.apply_async(args=[instance.id])
