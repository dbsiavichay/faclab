from functools import cached_property

from django.db import models
from django.utils.translation import gettext_lazy as _
from tree_queries.models import TreeNode

from apps.inventory.domain.choices import PriceTypes, ProductTypes


class ProductCategory(TreeNode):
    name = models.CharField(max_length=64, verbose_name=_("name"))
    parent = TreeNode._meta.get_field("parent")
    parent.verbose_name = _("parent category")

    class Meta:
        verbose_name = _("category")

    def __str__(self):
        return self.name


class Measure(models.Model):
    code = models.CharField(max_length=16, verbose_name=_("code"))
    name = models.CharField(max_length=64, verbose_name=_("name"))

    class Meta:
        verbose_name = _("measure")

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=16, verbose_name=_("code"))
    name = models.CharField(max_length=64, verbose_name=_("name"))
    short_name = models.CharField(max_length=16, verbose_name=_("short name"))
    description = models.TextField(verbose_name=_("description"))
    sku = models.CharField(max_length=32, blank=True, null=True)
    is_inventoried = models.BooleanField(default=True, verbose_name=_("is inventoried"))
    apply_iva = models.BooleanField(default=False, verbose_name=_("apply iva"))
    apply_ice = models.BooleanField(default=False, verbose_name=_("apply ice"))
    stock = models.FloatField(default=0, verbose_name=_("stock"))
    warehouse_location = models.TextField(
        blank=True, null=True, verbose_name=_("warehouse location")
    )
    type = models.CharField(
        max_length=2,
        choices=ProductTypes.choices,
        blank=True,
        null=True,
        verbose_name=_("type"),
    )
    category = models.ForeignKey(
        "inventory.ProductCategory",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_("category"),
    )
    measure = models.ForeignKey(
        "inventory.Measure",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_("unit of measure"),
    )
    provider = models.ForeignKey(
        "purchase.Provider",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_("provider"),
    )

    def __str__(self):
        return self.name

    @cached_property
    def cost_price(self):
        return self.prices.filter(type=PriceTypes.PURCHASE).first()

    @cached_property
    def sale_prices(self):
        return self.prices.filter(type=PriceTypes.SALE)


class ProductPrice(models.Model):
    type = models.CharField(
        max_length=2, choices=PriceTypes.choices, verbose_name=_("type")
    )
    amount = models.FloatField(verbose_name=_("amount"))
    revenue = models.FloatField(verbose_name=_("revenue"))
    product = models.ForeignKey(
        "inventory.Product", on_delete=models.CASCADE, related_name="prices"
    )

    @cached_property
    def gross_amount(self):
        if self.amount:
            return round(self.amount * 1.12, 5)

    @cached_property
    def percent_revenue(self):
        if self.amount and self.revenue:
            cost = self.amount - self.revenue
            return round((self.revenue * 100) / cost, 5)
