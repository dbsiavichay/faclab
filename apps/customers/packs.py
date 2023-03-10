from faclab.base import BasePack
from viewpack.decorators import register


@register("customers.Customer")
class CustomerPack(BasePack):
    list_fields = ("code_type", "code", "bussiness_name")
