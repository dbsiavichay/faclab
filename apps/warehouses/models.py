from django.db import models
from django.utils.translation import gettext_lazy as _
from tree_queries.models import TreeNode

from .enums import PriceTypes, ProductTypes


class ProductCategory(TreeNode):
    name = models.CharField(max_length=64, verbose_name=_("name"))

    def __str__(self):
        return self.name


class Measure(models.Model):
    code = models.CharField(max_length=16, verbose_name=_("code"))
    name = models.CharField(max_length=64, verbose_name=_("name"))

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=16, verbose_name=_("code"))
    name = models.CharField(max_length=64, verbose_name=_("name"))
    short_name = models.CharField(max_length=16, verbose_name=_("short name"))
    description = models.TextField(verbose_name=_("description"))
    is_inventoried = models.BooleanField(default=True, verbose_name=_("is inventoried"))
    apply_iva = models.BooleanField(default=False, verbose_name=_("apply iva"))
    apply_ice = models.BooleanField(default=False, verbose_name=_("apply ice"))
    stock = models.FloatField(default=0, verbose_name=_("stock"))
    type = models.CharField(
        max_length=2,
        choices=ProductTypes.choices,
        blank=True,
        null=True,
        verbose_name=_("type"),
    )
    category = models.ForeignKey(
        "warehouses.ProductCategory",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_("category"),
    )
    measure = models.ForeignKey(
        "warehouses.Measure",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_("unit of measure"),
    )

    def __str__(self):
        return self.name


class Price(models.Model):
    type = models.CharField(
        max_length=2, choices=PriceTypes.choices, verbose_name=_("type")
    )
    amount = models.FloatField(verbose_name=_("amount"))
    revenue = models.FloatField(verbose_name=_("revenue"))
    product = models.ForeignKey(
        "warehouses.Product", on_delete=models.CASCADE, related_name="prices"
    )
