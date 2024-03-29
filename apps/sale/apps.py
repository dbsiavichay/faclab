from django.apps import AppConfig

from faclab import container


class SaleAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.sale"

    def ready(self):
        container.wire(modules=[".forms"])
