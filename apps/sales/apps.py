from django.apps import AppConfig

from faclab import container


class SalesAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.sales"

    def ready(self):
        container.wire(modules=[".forms"])
