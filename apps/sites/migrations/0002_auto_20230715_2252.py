# Generated by Django 3.2.16 on 2023-07-15 22:52

from django.db import migrations


def create_empty_config(apps, schema_editor):
    Config = apps.get_model("sites", "Config")
    Config.objects.create(sri_config=dict())


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            code=create_empty_config, reverse_code=migrations.RunPython.noop
        )
    ]
