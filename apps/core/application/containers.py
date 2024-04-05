from dependency_injector import containers, providers

from apps.core.infra.adapters import MenuAdapter, SiteAdapter


class CoreContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    site_adapter = providers.Singleton(SiteAdapter)
    menu_adapter = providers.Singleton(MenuAdapter)
