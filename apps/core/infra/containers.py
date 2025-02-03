from dependency_injector import containers, providers

from apps.core.application.services import SealifyService, SignatureService
from apps.core.application.usecases import RetrieveSignatureUseCase
from apps.core.infra.adapters import SealifyAdapter
from apps.core.infra.repositories import (
    MenuRepositoryImpl,
    SignatureRepositoryImpl,
    SiteRepositoryImpl,
)


class CoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Repositories
    site_repository = providers.Singleton(SiteRepositoryImpl)
    signature_repository = providers.Singleton(SignatureRepositoryImpl)
    menu_repository = providers.Singleton(MenuRepositoryImpl)

    # Adapters
    sealify_adapter = providers.Singleton(
        SealifyAdapter, base_url=config.SEALIFY_BASE_URL
    )

    # Usecases
    retrieve_signature_usecase = providers.Singleton(RetrieveSignatureUseCase)

    # Services
    signature_service = providers.Singleton(
        SignatureService,
        signature_repository=signature_repository,
        retrieve_signature_usecase=retrieve_signature_usecase,
    )

    sealify_service = providers.Singleton(SealifyService, sealify_port=sealify_adapter)
