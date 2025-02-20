from dependency_injector import containers, providers

from apps.core.application.services import SealifyService
from apps.core.infra.adapters import SealifyAdapter
from apps.core.infra.repositories import MenuRepositoryImpl, SiteRepositoryImpl


class CoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Repositories
    site_repository = providers.Singleton(SiteRepositoryImpl)
    menu_repository = providers.Singleton(MenuRepositoryImpl)

    # Adapters
    sealify_adapter = providers.Singleton(
        SealifyAdapter, base_url=config.SEALIFY_BASE_URL
    )

    # Services
    sealify_service = providers.Singleton(SealifyService, sealify_port=sealify_adapter)
