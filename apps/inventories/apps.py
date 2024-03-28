from django.apps import AppConfig

from faclab import container


class InventoriesAppConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "apps.inventories"

    def ready(self):
        container.wire(modules=[".services"])
