from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.sales.validators import customer_code_validator


class Provider(models.Model):
    code = models.CharField(
        max_length=13,
        unique=True,
        validators=[MinLengthValidator(limit_value=13), customer_code_validator],
        verbose_name=_("identification"),
    )
    bussiness_name = models.CharField(max_length=128, verbose_name=_("bussiness name"))
    contact_name = models.CharField(max_length=128, verbose_name=_("contact name"))
    address = models.TextField(verbose_name=_("address"))
    phone = models.CharField(max_length=16, verbose_name=_("phone"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("email"))
    website = models.CharField(
        max_length=32, blank=True, null=True, verbose_name=_("website")
    )

    class Meta:
        verbose_name = _("provider")
        verbose_name_plural = _("providers")

    def __str__(self):
        return self.bussiness_name
