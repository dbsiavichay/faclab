from dependency_injector import containers, providers

from apps.inventory.application.services import InventoryService
from apps.inventory.application.usecases import CreateEntryStockMoveUseCase
from apps.inventory.infra.repositories import (
    MenuRepositoryImpl,
    ProductRepositoryImpl,
    StockMoveRepositoryImpl,
)


class InventoryContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Repositories
    menu_repository = providers.Singleton(MenuRepositoryImpl)
    stock_move_repository = providers.Singleton(StockMoveRepositoryImpl)
    product_repository = providers.Singleton(ProductRepositoryImpl)

    # Usecases
    create_entry_stock_move_usecase = providers.Singleton(
        CreateEntryStockMoveUseCase,
        stock_move_repository=stock_move_repository,
        product_repository=product_repository,
    )

    # Services
    inventory_service = providers.Singleton(
        InventoryService,
        create_entry_stock_move_usecase=create_entry_stock_move_usecase,
    )
