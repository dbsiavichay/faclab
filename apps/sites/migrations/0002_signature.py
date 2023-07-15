# Generated by Django 3.2.16 on 2023-07-15 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Signature",
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
                    "subject_name",
                    models.CharField(max_length=64, verbose_name="subject"),
                ),
                (
                    "serial_number",
                    models.CharField(
                        max_length=64, unique=True, verbose_name="serial number"
                    ),
                ),
                ("issue_date", models.DateTimeField(verbose_name="issue date")),
                ("expiry_date", models.DateTimeField(verbose_name="expiry date")),
                ("cert", models.TextField()),
                ("key", models.TextField()),
            ],
        ),
    ]
