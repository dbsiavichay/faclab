# Generated by Django 3.2.16 on 2023-10-02 14:46

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import apps.sales.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Measure",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=16, verbose_name="code")),
                ("name", models.CharField(max_length=64, verbose_name="name")),
            ],
            options={
                "verbose_name": "measure",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=16, verbose_name="code")),
                ("name", models.CharField(max_length=64, verbose_name="name")),
                (
                    "short_name",
                    models.CharField(max_length=16, verbose_name="short name"),
                ),
                ("description", models.TextField(verbose_name="description")),
                ("sku", models.CharField(blank=True, max_length=32, null=True)),
                (
                    "is_inventoried",
                    models.BooleanField(default=True, verbose_name="is inventoried"),
                ),
                (
                    "apply_iva",
                    models.BooleanField(default=False, verbose_name="apply iva"),
                ),
                (
                    "apply_ice",
                    models.BooleanField(default=False, verbose_name="apply ice"),
                ),
                ("stock", models.FloatField(default=0, verbose_name="stock")),
                (
                    "warehouse_location",
                    models.TextField(
                        blank=True, null=True, verbose_name="warehouse location"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[("p", "Producto"), ("s", "Servicio")],
                        max_length=2,
                        null=True,
                        verbose_name="type",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Provider",
            fields=[
                (
                    "id",
                    models.AutoField(
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
                            apps.sales.validators.customer_code_validator,
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
                    models.AutoField(
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
                        to="inventories.provider",
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
                    models.AutoField(
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
                        to="inventories.purchase",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="inventories.product",
                        verbose_name="product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductPrice",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("p", "purchase"), ("s", "sale")],
                        max_length=2,
                        verbose_name="type",
                    ),
                ),
                ("amount", models.FloatField(verbose_name="amount")),
                ("revenue", models.FloatField(verbose_name="revenue")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prices",
                        to="inventories.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, verbose_name="name")),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="inventories.productcategory",
                        verbose_name="parent",
                    ),
                ),
            ],
            options={
                "verbose_name": "category",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inventories.productcategory",
                verbose_name="category",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="measure",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inventories.measure",
                verbose_name="unit of measure",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="provider",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inventories.provider",
                verbose_name="provider",
            ),
        ),
    ]
