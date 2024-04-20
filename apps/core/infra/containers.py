from dependency_injector import containers, providers

from apps.core.application.services import SignatureService
from apps.core.application.usecases import RetrieveSignatureUseCase
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

    # Usecases
    retrieve_signature_usecase = providers.Singleton(RetrieveSignatureUseCase)

    # Services
    signature_service = providers.Singleton(
        SignatureService,
        signature_repository=signature_repository,
        retrieve_signature_usecase=retrieve_signature_usecase,
    )
