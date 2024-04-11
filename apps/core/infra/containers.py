from dependency_injector import containers, providers

from apps.core.infra.repositories import MenuRepositoryImpl, SiteRepositoryImpl


class CoreContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    site_repository = providers.Singleton(SiteRepositoryImpl)
    menu_repository = providers.Singleton(MenuRepositoryImpl)
