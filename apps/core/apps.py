from django.apps import AppConfig

from faclab import container


class CoreAppConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "apps.core"

    def ready(self):
        container.wire(
            modules=[".application.main_menu", ".infra.adapters", ".infra.forms"]
        )
