from django.db import models
from django.utils.translation import gettext_lazy as _


class Environments(models.IntegerChoices):
    TESTING = 1, _("testing").capitalize()
    PRODUCTION = 2, _("production").capitalize()


class Emissions(models.IntegerChoices):
    NORMAL = 1, _("normal").capitalize()
