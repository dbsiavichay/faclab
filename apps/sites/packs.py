from faclab.base import BasePack
from viewpack.decorators import register
from viewpack.enums import PackViews

from .forms import ConfigForm, SignatureForm
from .mixins import ConfigFormMixin


@register("sites.Signature")
class SignaturePack(BasePack):
    form_class = SignatureForm
    list_fields = ("subject_name", "serial_number", "issue_date", "expiry_date")
    allowed_views = (PackViews.LIST, PackViews.CREATE, PackViews.DELETE)


@register("sites.Config")
class ConfigPack(BasePack):
    form_class = ConfigForm
    list_fields = tuple(f"sri_config__{field}" for field in ConfigForm.Meta.fields[:3])
    detail_fields = list_fields
    default_labels = {
        f"sri_config__{name}": field.label
        for name, field in tuple(ConfigForm.declared_fields.items())[:3]
    }
    form_mixins = (ConfigFormMixin,)
