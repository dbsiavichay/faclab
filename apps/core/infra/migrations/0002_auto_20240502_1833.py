# Generated by Django 3.2.16 on 2024-05-02 18:33

from django.db import migrations


def create_empty_config(apps, schema_editor):
    Site = apps.get_model("core", "Site")
    Site.objects.create(sri_config=dict())


def create_default_taxes(apps, schema_editor):
    Tax = apps.get_model("core", "Tax")
    tax_list = [
        ("0", "0%", 0),
        ("2", "12%", 12),
        ("3", "14%", 14),
        ("4", "15%", 15),
        ("5", "5%", 5),
        ("6", "NO OBJETO DE IMPUESTO", 0),
        ("7", "EXENTO DE IVA", 0),
        ("10", "13%", 13),
    ]
    taxes = [Tax(code=code, name=name, fee=fee) for code, name, fee in tax_list]
    Tax.objects.bulk_create(taxes)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            code=create_empty_config, reverse_code=migrations.RunPython.noop
        ),
        migrations.RunPython(
            code=create_default_taxes, reverse_code=migrations.RunPython.noop
        ),
    ]
