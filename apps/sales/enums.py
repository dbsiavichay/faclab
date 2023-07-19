from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class VoucherStatuses(TextChoices):
    GENERATED = "gen", _("generated")
    SIGNED = "sig", _("signed")
    VALIDATED = "val", _("validated")
    AUTHORIZED = "aut", _("authorized")
