from dependency_injector import containers, providers

from apps.core.infra.adapters import MenuAdapter, SiteAdapter


class CoreContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    site_service = providers.Singleton(SiteAdapter)
    menu_service = providers.Singleton(MenuAdapter)
