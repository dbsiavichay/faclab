from dependency_injector import containers, providers

from apps.sites.application.services import ConfigService


class SitesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    config_service = providers.Singleton(ConfigService)
