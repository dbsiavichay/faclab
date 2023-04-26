# Generated by Django 3.2.16 on 2023-04-26 03:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("warehouses", "0001_initial"),
        ("sales", "0002_auto_20230419_2331"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(verbose_name="date")),
                (
                    "company_code",
                    models.CharField(max_length=3, verbose_name="company code"),
                ),
                (
                    "company_point_sale_code",
                    models.CharField(
                        max_length=3, verbose_name="company point sale code"
                    ),
                ),
                ("sequence", models.CharField(max_length=9, verbose_name="sequence")),
                ("subtotal", models.FloatField(default=0, verbose_name="subtotal")),
                ("tax", models.FloatField(default=0, verbose_name="tax")),
                (
                    "total",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=10, verbose_name="total"
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="sales.customer",
                        verbose_name="customer",
                    ),
                ),
            ],
            options={
                "unique_together": {
                    ("company_code", "company_point_sale_code", "sequence")
                },
            },
        ),
        migrations.CreateModel(
            name="VoucherType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=2, unique=True, verbose_name="code"),
                ),
                ("name", models.CharField(max_length=32, verbose_name="name")),
                (
                    "current",
                    models.PositiveIntegerField(default=0, verbose_name="current"),
                ),
                (
                    "ends",
                    models.PositiveIntegerField(default=999999999, verbose_name="ends"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InvoiceLine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.FloatField(default=1, verbose_name="quantity")),
                ("unit_price", models.FloatField(verbose_name="unit price")),
                ("subtotal", models.FloatField(verbose_name="subtotal")),
                ("tax", models.FloatField(default=0, verbose_name="tax")),
                ("total", models.FloatField(verbose_name="total")),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lines",
                        to="sales.invoice",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="warehouses.product",
                        verbose_name="product",
                    ),
                ),
            ],
        ),
    ]