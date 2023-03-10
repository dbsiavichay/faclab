from faclab.base import BasePack
from viewpack.decorators import register


@register("account.User")
class UserPack(BasePack):
    list_fields = (
        "email",
        "username",
        "get_full_name:nombre completo",
    )
