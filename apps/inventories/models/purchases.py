from django.db import models
from django.utils.translation import gettext_lazy as _


class Purchase(models.Model):
    date = models.DateField(verbose_name=_("date"))
    invoice_number = models.CharField(max_length=32, verbose_name=_("invoice number"))
    subtotal = models.FloatField(default=0, verbose_name=_("subtotal"))
    tax = models.FloatField(default=0, verbose_name=_("tax"))
    total = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name=_("total")
    )
    provider = models.ForeignKey(
        "inventories.Provider", on_delete=models.PROTECT, verbose_name=_("provider")
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
        "inventories.Product", on_delete=models.PROTECT, verbose_name=_("product")
    )
    invoice = models.ForeignKey(
        "inventories.Purchase", on_delete=models.CASCADE, related_name="lines"
    )
