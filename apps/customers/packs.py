from faclab.base import BasePack
from viewpack.decorators import register

from .forms import CustomerForm


@register("customers.Customer")
class CustomerPack(BasePack):
    form_class = CustomerForm
    list_fields = ("code_type", "code", "bussiness_name")
    # detail_fields = ("first_name",)
