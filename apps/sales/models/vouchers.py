from django.db import models
from django.utils.translation import gettext_lazy as _


class VoucherType(models.Model):
    code = models.CharField(max_length=2, unique=True, verbose_name=_("code"))
    name = models.CharField(max_length=32, verbose_name=_("name"))
    current = models.PositiveIntegerField(default=0, verbose_name=_("current"))
    ends = models.PositiveIntegerField(default=999999999, verbose_name=_("ends"))
