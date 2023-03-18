from faclab.base import BasePack
from viewpack.decorators import register

from .forms import ConfigForm


@register("sites.Config")
class ConfigPack(BasePack):
    form_class = ConfigForm
    list_fields = ("sri_config",)
