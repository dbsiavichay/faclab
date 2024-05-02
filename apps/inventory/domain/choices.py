from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ProductType(TextChoices):
    PRODUCT = "p", _("product").capitalize()
    SERVICE = "s", _("service").capitalize()


class PriceType(TextChoices):
    PURCHASE = "p", _("purchase")
    SALE = "s", _("sale")
