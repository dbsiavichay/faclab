from django.db import models
from django.utils.translation import gettext_lazy as _


class Signature(models.Model):
    subject_name = models.CharField(max_length=64, verbose_name=_("subject"))
    serial_number = models.CharField(
        max_length=64, unique=True, verbose_name=_("serial number")
    )
    issue_date = models.DateTimeField(verbose_name=_("issue date"))
    expiry_date = models.DateTimeField(verbose_name=_("expiry date"))
    cert = models.TextField()
    key = models.TextField()

    def __str__(self) -> str:
        return f"{self.subject_name} - {self.serial_number}"


class Config(models.Model):
    sri_config = models.JSONField(default=dict)
