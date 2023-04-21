from django.db import models
from django.utils.translation import gettext_lazy as _


class Invoice(models.Model):
    date = models.DateField(verbose_name=_("date"))
    number = models.CharField(max_length=9, unique=True, verbose_name=_("number"))
    subtotal = models.FloatField(default=0, verbose_name=_("subtotal"))
    tax = models.FloatField(default=0, verbose_name=_("tax"))
    total = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name=_("total")
    )
    customer = models.ForeignKey(
        "sales.Customer", on_delete=models.PROTECT, verbose_name=_("customer")
    )

    def __str__(self):
        return _("invoice # {0}").format(self.number).capitalize()


class InvoiceLine(models.Model):
    quantity = models.FloatField(default=1, verbose_name=_("quantity"))
    unit_price = models.FloatField(verbose_name=_("unit price"))
    subtotal = models.FloatField(verbose_name=_("subtotal"))
    tax = models.FloatField(default=0, verbose_name=_("tax"))
    total = models.FloatField(verbose_name=_("total"))
    product = models.ForeignKey(
        "warehouses.Product", on_delete=models.PROTECT, verbose_name=_("product")
    )
    invoice = models.ForeignKey(
        "sales.Invoice", on_delete=models.CASCADE, related_name="lines"
    )
