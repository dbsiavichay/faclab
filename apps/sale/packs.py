import pytz
from dependency_injector.wiring import Provide, inject
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.sale.infra.tasks import send_invoice_task
from faclab.base import BasePack
from viewpack.decorators import register
from viewpack.enums import PackViews

from .application.services import InvoiceService
from .domain.entities import CustomerEntity, InvoiceEntity
from .infra.forms import (
    CustomerForm,
    InvoiceForm,
    InvoiceLineFormset,
    InvoicePaymentFormset,
)


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
        timezone = pytz.timezone(settings.TIME_ZONE)
        customer = instance.customer
        customer_entity = CustomerEntity(
            code_type_code=customer.code_type.code, **customer.__dict__
        )
        invoice_lines = invoice_service.invoiceline_repository.find_by_invoice(
            instance.id
        )
        invoice_dict = {
            **instance.__dict__,
            "date": instance.date.astimezone(timezone),
        }
        invoice_entity = InvoiceEntity(
            customer=customer_entity, lines=invoice_lines, **invoice_dict
        )
        invoice_service.update_invoice_xml(invoice_entity)
        invoice_service.sign_invoice_xml(invoice_entity, update_on_db=True)
        send_invoice_task.apply_async(args=[instance.id])
