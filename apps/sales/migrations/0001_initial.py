# Generated by Django 3.2.16 on 2023-04-19 15:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("warehouses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                        max_length=16,
                        unique=True,
                        verbose_name="identification",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="last name"
                    ),
                ),
                (
                    "bussiness_name",
                    models.CharField(max_length=128, verbose_name="bussiness name"),
                ),
                (
                    "address",
                    models.TextField(blank=True, null=True, verbose_name="address"),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=16, null=True, verbose_name="phone"
                    ),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="email")),
            ],
        ),
        migrations.CreateModel(
            name="CustomerCodeType",
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
                ("code", models.CharField(max_length=2, unique=True)),
                ("name", models.CharField(max_length=32)),
                ("length", models.PositiveSmallIntegerField()),
            ],
        ),
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
                ("number", models.CharField(max_length=9)),
                ("subtotal", models.FloatField(default=0, verbose_name="subtotal")),
                (
                    "tax",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="tax"
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="tax"
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
                ("total", models.FloatField(verbose_name="subtotal")),
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
        migrations.AddField(
            model_name="customer",
            name="code_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="sales.customercodetype",
                verbose_name="code type",
            ),
        ),
    ]
