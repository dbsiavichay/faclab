from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.sales.enums import VoucherStatuses


class Invoice(models.Model):
    issue_date = models.DateTimeField(auto_now_add=True, verbose_name=_("issue date"))
    authorization_date = models.DateTimeField(
        null=True, verbose_name=_("authorization date")
    )
    code = models.CharField(max_length=64, null=True, verbose_name=_("access code"))
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
    status = models.CharField(
        max_length=4,
        choices=VoucherStatuses.choices,
        default=VoucherStatuses.GENERATED,
        verbose_name=_("status"),
    )
    file = models.FileField(upload_to="vouchers", null=True)
    signed_file = models.FileField(upload_to="vouchers", null=True)
    authorized_file = models.FileField(upload_to="vouchers", null=True)
    errors = models.JSONField(default=dict)
    customer = models.ForeignKey(
        "sales.Customer", on_delete=models.PROTECT, verbose_name=_("customer")
    )

    class Meta:
        unique_together = ("company_code", "company_point_sale_code", "sequence")
        verbose_name = _("invoice")

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
