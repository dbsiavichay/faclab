from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.sale.application.validators import customer_code_validator


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


class Purchase(models.Model):
    date = models.DateField(verbose_name=_("date"))
    invoice_number = models.CharField(max_length=32, verbose_name=_("invoice number"))
    subtotal = models.FloatField(default=0, verbose_name=_("subtotal"))
    tax = models.FloatField(default=0, verbose_name=_("tax"))
    total = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name=_("total")
    )
    provider = models.ForeignKey(
        "purchase.Provider", on_delete=models.PROTECT, verbose_name=_("provider")
    )

    class Meta:
        verbose_name = _("purchase")

    def __str__(self):
        return _("purchase # {0}").format(self.invoice_number).capitalize()


class PurchaseLine(models.Model):
    quantity = models.FloatField(default=1, verbose_name=_("quantity"))
    unit_price = models.FloatField(verbose_name=_("unit price"))
    subtotal = models.FloatField(verbose_name=_("subtotal"))
    tax = models.FloatField(default=0, verbose_name=_("tax"))
    total = models.FloatField(verbose_name=_("total"))
    product = models.ForeignKey(
        "inventory.Product", on_delete=models.PROTECT, verbose_name=_("product")
    )
    invoice = models.ForeignKey(
        "purchase.Purchase", on_delete=models.CASCADE, related_name="lines"
    )
