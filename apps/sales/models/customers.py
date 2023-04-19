from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomerCodeType(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=32)
    length = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    code = models.CharField(
        max_length=16,
        unique=True,
        verbose_name=_("identification"),
    )
    first_name = models.CharField(
        max_length=64, blank=True, null=True, verbose_name=_("first name")
    )
    last_name = models.CharField(
        max_length=64, blank=True, null=True, verbose_name=_("last name")
    )
    bussiness_name = models.CharField(max_length=128, verbose_name=_("bussiness name"))
    address = models.TextField(blank=True, null=True, verbose_name=_("address"))
    phone = models.CharField(
        max_length=16, blank=True, null=True, verbose_name=_("phone")
    )
    email = models.EmailField(verbose_name=_("email"))
    code_type = models.ForeignKey(
        "sales.CustomerCodeType", on_delete=models.PROTECT, verbose_name=_("code type")
    )

    def __str__(self):
        return self.bussiness_name
