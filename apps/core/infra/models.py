from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.domain.choices import TaxType


class Site(models.Model):
    sri_config = models.JSONField(default=dict)


class Tax(models.Model):
    type = models.CharField(
        max_length=4,
        choices=TaxType.choices,
        default=TaxType.IVA,
        verbose_name=_("type"),
    )
    code = models.CharField(max_length=4, verbose_name=_("code"))
    name = models.CharField(max_length=64, verbose_name=_("name"))
    fee = models.PositiveSmallIntegerField(verbose_name=_("fee"))

    class Meta:
        verbose_name = _("tax")
        verbose_name_plural = _("taxes")

    def __str__(self) -> str:
        return self.name

    @property
    def decimal_fee(self):
        return self.fee / 100

    @property
    def decimal_factor(self):
        return 1 + self.decimal_fee
