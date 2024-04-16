from dependency_injector import containers, providers

from apps.core.infra.repositories import (
    MenuRepositoryImpl,
    SignatureRepositoryImpl,
    SiteRepositoryImpl,
)


class CoreContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    site_repository = providers.Singleton(SiteRepositoryImpl)
    signature_repository = providers.Singleton(SignatureRepositoryImpl)
    menu_repository = providers.Singleton(MenuRepositoryImpl)
