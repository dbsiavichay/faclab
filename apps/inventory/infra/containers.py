from dependency_injector import containers, providers

from apps.inventory.infra.repositories import MenuRepositoryImpl


class InventoryContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Repositories
    menu_repository = providers.Singleton(MenuRepositoryImpl)
