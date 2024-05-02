from faclab.base import BasePack
from viewpack.decorators import register
from viewpack.enums import PackViews

from .infra.forms import SignatureForm, SiteForm
from .infra.mixins import SiteFormMixin


@register("core.Signature")
class SignaturePack(BasePack):
    form_class = SignatureForm
    list_fields = ("subject_name", "serial_number", "issue_date", "expiry_date")
    allowed_views = (PackViews.LIST, PackViews.CREATE, PackViews.DELETE)


@register("core.Tax")
class TaxPack(BasePack):
    list_fields = ("code", "name", "fee")


@register("core.Site")
class SitePack(BasePack):
    form_class = SiteForm
    allowed_views = (PackViews.UPDATE,)
    default_labels = {
        f"sri_config__{name}": field.label
        for name, field in tuple(SiteForm.declared_fields.items())[:3]
    }
    form_mixins = (SiteFormMixin,)
