from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class CodeTypes(TextChoices):
    CHARTER = "cht", _("charter")
    RUC = "ruc", _("ruc")
    PASSPORT = "pst", _("passport")
    FOREIGN = "fgn", _("foreign identification")
