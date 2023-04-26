from django.db import models
from django.utils.translation import gettext_lazy as _


class VoucherType(models.Model):
    code = models.CharField(max_length=2, unique=True, verbose_name=_("code"))
    name = models.CharField(max_length=32, verbose_name=_("name"))
    current = models.PositiveIntegerField(default=0, verbose_name=_("current"))
    ends = models.PositiveIntegerField(default=999999999, verbose_name=_("ends"))


class Invoice(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name=_("date"))
    company_code = models.CharField(max_length=3, verbose_name=_("company code"))
    company_point_sale_code = models.CharField(
        max_length=3, verbose_name=_("company point sale code")
    )
    sequence = models.CharField(max_length=9, verbose_name=_("sequence"))
    subtotal = models.FloatField(default=0, verbose_name=_("subtotal"))
    tax = models.FloatField(default=0, verbose_name=_("tax"))
    total = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name=_("total")
    )
    customer = models.ForeignKey(
        "sales.Customer", on_delete=models.PROTECT, verbose_name=_("customer")
    )

    class Meta:
        unique_together = ("company_code", "company_point_sale_code", "sequence")

    def __str__(self):
        return _("invoice # {0}").format(self.number).capitalize()

    @property
    def number(self):
        return "-".join(
            (self.company_code, self.company_point_sale_code, self.sequence)
        )


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
