from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class VoucherStatus(TextChoices):
    GENERATED = "gen", _("generated")
    SIGNED = "sig", _("signed")
    VALIDATED = "val", _("validated")
    AUTHORIZED = "aut", _("authorized")


class PaymentType(TextChoices):
    CASH = "01", _("cash")
    CREDIT_CARD = "19", _("credit card")
    BANK = "20", _("deposit/transfer")
