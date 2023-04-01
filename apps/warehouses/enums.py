from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ProductTypes(TextChoices):
    PRODUCT = "p", _("product")
    SERVICE = "s", _("service")


class PriceTypes(TextChoices):
    PURCHASE = "p", _("purchase")
    SALE = "s", _("sale")
