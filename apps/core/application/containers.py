from dependency_injector import containers, providers

from .services import SiteService


class CoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    site_service = providers.Singleton(SiteService)
