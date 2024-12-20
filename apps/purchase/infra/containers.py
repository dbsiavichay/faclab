from dependency_injector import containers, providers

from apps.purchase.application.services import PurchaseService
from apps.purchase.application.usecases import (
    CalculatePurchaseLineTotalUseCase,
    CalculatePurchaseTotalUseCase,
)
from apps.purchase.infra.repositories import (
    MenuRepositoryImpl,
    PurchaseLineRepositoryImpl,
    PurchaseRepositoryImpl,
)


class PurchaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Repositories
    menu_repository = providers.Singleton(MenuRepositoryImpl)
    purchase_repository = providers.Singleton(PurchaseRepositoryImpl)
    purchaseline_repository = providers.Singleton(PurchaseLineRepositoryImpl)

    # Usecases
    calculate_purchase_total_usecase = providers.Singleton(
        CalculatePurchaseTotalUseCase, purchase_repository=purchase_repository
    )
    calculate_purchaseline_total_usecase = providers.Singleton(
        CalculatePurchaseLineTotalUseCase
    )

    # Services
    purchase_service = providers.Singleton(
        PurchaseService,
        purchase_repository=purchase_repository,
        purchaseline_repository=purchaseline_repository,
        calculate_purchase_total_usecase=calculate_purchase_total_usecase,
        calculate_purchaseline_total_usecase=calculate_purchaseline_total_usecase,
    )
