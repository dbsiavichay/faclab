# Generated by Django 3.2.16 on 2023-04-19 23:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
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
                        max_length=16, unique=True, verbose_name="identification"
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
                (
                    "code_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="sale.customercodetype",
                        verbose_name="code type",
                    ),
                ),
            ],
        ),
    ]
