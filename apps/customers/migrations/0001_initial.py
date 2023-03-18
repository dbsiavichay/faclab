# Generated by Django 3.2.16 on 2023-03-13 19:35

from django.db import migrations, models

import apps.customers.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

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
                    "code_type",
                    models.CharField(
                        choices=[
                            ("cht", "charter"),
                            ("ruc", "ruc"),
                            ("pst", "passport"),
                            ("fgn", "foreign identification"),
                        ],
                        max_length=4,
                        verbose_name="code type",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        max_length=16,
                        unique=True,
                        validators=[apps.customers.validators.code_validator],
                        verbose_name="code",
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
    ]