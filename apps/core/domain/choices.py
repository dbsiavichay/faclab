from django.db import models
from django.utils.translation import gettext_lazy as _


class Environment(models.IntegerChoices):
    TESTING = 1, _("testing").capitalize()
    PRODUCTION = 2, _("production").capitalize()


class EmissionType(models.IntegerChoices):
    NORMAL = 1, _("normal").capitalize()


class TaxType(models.TextChoices):
    IVA = "2", _("value added tax").capitalize()
    ICE = "3", _("excise tax").capitalize()
