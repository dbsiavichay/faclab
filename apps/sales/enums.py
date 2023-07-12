from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class VoucherStatuses(TextChoices):
    GENERATED = "gen", _("generated").upper()
    SIGNED = "sig", _("signed").upper()
    VALIDATED = "val", _("validated").upper()
    AUTHORIZED = "aut", _("authorized").upper()
