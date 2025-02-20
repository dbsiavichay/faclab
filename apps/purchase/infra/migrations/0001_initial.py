# Generated by Django 3.2.16 on 2025-02-20 21:13

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import apps.sale.application.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Provider",
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
                    models.CharField(
                        max_length=13,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=13),
                            apps.sale.application.validators.customer_code_validator,
                        ],
                        verbose_name="identification",
                    ),
                ),
                (
                    "bussiness_name",
                    models.CharField(max_length=128, verbose_name="bussiness name"),
                ),
                (
                    "contact_name",
                    models.CharField(max_length=128, verbose_name="contact name"),
                ),
                ("address", models.TextField(verbose_name="address")),
                ("phone", models.CharField(max_length=16, verbose_name="phone")),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, verbose_name="email"
                    ),
                ),
                (
                    "website",
                    models.CharField(
                        blank=True, max_length=32, null=True, verbose_name="website"
                    ),
                ),
            ],
            options={
                "verbose_name": "provider",
                "verbose_name_plural": "providers",
            },
        ),
        migrations.CreateModel(
            name="Purchase",
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
                    "invoice_number",
                    models.CharField(max_length=32, verbose_name="invoice number"),
                ),
                ("subtotal", models.FloatField(default=0, verbose_name="subtotal")),
                ("tax", models.FloatField(default=0, verbose_name="tax")),
                (
                    "total",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=10, verbose_name="total"
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="purchase.provider",
                        verbose_name="provider",
                    ),
                ),
            ],
            options={
                "verbose_name": "purchase",
            },
        ),
        migrations.CreateModel(
            name="PurchaseLine",
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
                        to="purchase.purchase",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="inventory.product",
                        verbose_name="product",
                    ),
                ),
            ],
        ),
    ]
