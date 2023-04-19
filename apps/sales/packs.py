from faclab.base import BasePack
from viewpack.decorators import register

from .forms import CustomerForm


@register("sales.Customer")
class CustomerPack(BasePack):
    form_class = CustomerForm
    list_fields = ("code_type", "code", "bussiness_name")
    detail_fields = CustomerForm.Meta.fieldsets
