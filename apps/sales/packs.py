from faclab.base import BasePack
from viewpack.decorators import register

from .forms import CustomerForm, InvoiceForm, InvoiceLineFormset


@register("sales.Customer")
class CustomerPack(BasePack):
    form_class = CustomerForm
    list_fields = ("code_type", "code", "bussiness_name")
    detail_fields = CustomerForm.Meta.fieldsets


@register("sales.Invoice")
class InvoicePack(BasePack):
    form_class = InvoiceForm
    inlines = {"lines": InvoiceLineFormset}
    list_fields = ("customer", "number", "date", "subtotal", "tax", "total")
    detail_fields = (("customer", "date"),)
    form_template_name = None
    detail_template_name = None
