from dependency_injector import containers, providers

from .services import MenuService, SiteService


class CoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    site_service = providers.Singleton(SiteService)
    menu_service = providers.Singleton(MenuService)
