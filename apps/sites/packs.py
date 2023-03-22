from faclab.base import BasePack
from viewpack.decorators import register

from .forms import ConfigForm
from .mixins import ConfigFormMixin


@register("sites.Config")
class ConfigPack(BasePack):
    form_class = ConfigForm
    list_fields = (f"sri_config__{field}" for field in ConfigForm.Meta.fields[:3])
    default_labels = {
        f"sri_config__{name}": field.label
        for name, field in tuple(ConfigForm.declared_fields.items())[:3]
    }
    form_mixins = (ConfigFormMixin,)
