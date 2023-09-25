# Generated by Django 3.2.16 on 2023-09-25 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventories", "0001_initial"),
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
                (
                    "issue_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="issue date"),
                ),
                (
                    "authorization_date",
                    models.DateTimeField(null=True, verbose_name="authorization date"),
                ),
                (
                    "code",
                    models.CharField(
                        max_length=64, null=True, verbose_name="access code"
                    ),
                ),
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
                    "status",
                    models.CharField(
                        choices=[
                            ("gen", "generated"),
                            ("sig", "signed"),
                            ("val", "validated"),
                            ("aut", "authorized"),
                        ],
                        default="gen",
                        max_length=4,
                        verbose_name="status",
                    ),
                ),
                ("file", models.FileField(null=True, upload_to="vouchers/invoices")),
                ("errors", models.JSONField(default=dict)),
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
                "verbose_name": "invoice",
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
            options={
                "verbose_name": "voucher",
            },
        ),
        migrations.CreateModel(
            name="InvoicePayment",
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
                    "type",
                    models.CharField(
                        choices=[
                            ("01", "cash"),
                            ("19", "credit card"),
                            ("20", "deposit/transfer"),
                        ],
                        default="01",
                        max_length=2,
                        verbose_name="type",
                    ),
                ),
                ("amount", models.FloatField(verbose_name="amount")),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="sales.invoice",
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
                        to="inventories.product",
                        verbose_name="product",
                    ),
                ),
            ],
        ),
    ]
