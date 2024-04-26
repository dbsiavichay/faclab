from dependency_injector import containers, providers

from apps.inventory.application.services import PurchaseService
from apps.inventory.application.usecases import (
    CalculatePurchaseLineTotalUseCase,
    CalculatePurchaseTotalUseCase,
)
from apps.inventory.infra.repositories import (
    MenuRepositoryImpl,
    PurchaseLineRepositoryImpl,
    PurchaseRepositoryImpl,
)


class InventoryContainer(containers.DeclarativeContainer):
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
