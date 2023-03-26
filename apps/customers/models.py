from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .enums import CodeTypes
from .validators import code_validator

User = get_user_model()


class Customer(models.Model):
    code_type = models.CharField(
        choices=CodeTypes.choices, max_length=4, verbose_name=_("code type")
    )
    code = models.CharField(
        max_length=16, validators=[code_validator], unique=True, verbose_name=_("code")
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

    def __str__(self):
        return self.bussiness_name
