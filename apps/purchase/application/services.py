from dependency_injector.wiring import Provide, inject

from apps.core.domain.repositories import SiteRepository
from apps.purchase.application.usecases import (
    CalculatePurchaseLineTotalUseCase,
    CalculatePurchaseTotalUseCase,
)
from apps.purchase.domain.entities import PurchaseLineEntity
from apps.purchase.domain.repositories import PurchaseLineRepository, PurchaseRepository


class PurchaseService:
    @inject
    def __init__(
        self,
        purchase_repository: PurchaseRepository,
        purchaseline_repository: PurchaseLineRepository,
        calculate_purchase_total_usecase: CalculatePurchaseTotalUseCase,
        calculate_purchaseline_total_usecase: CalculatePurchaseLineTotalUseCase,
        site_repository: SiteRepository = Provide["core_package.site_repository"],
    ) -> None:
        self.purchase_repository = purchase_repository
        self.purchaseline_repository = purchaseline_repository
        self.calculate_purchase_total_usecase = calculate_purchase_total_usecase
        self.calculate_purchaseline_total_usecase = calculate_purchaseline_total_usecase
        self.site_repository = site_repository

    def update_purchase_total(
        self, purchase_entity: PurchaseLineEntity, update_on_db: bool = False
    ) -> PurchaseLineEntity:
        sri_config = self.site_repository.get_sri_config()
        purchase_entity = self.calculate_purchase_total_usecase.execute(
            purchase_entity, sri_config
        )

        if update_on_db:
            self.purchase_repository.save(
                purchase_entity, update_fields=["subtotal", "tax", "total"]
            )

        return purchase_entity

    def update_purchase_line_total(
        self, purchaseline_entity: PurchaseLineEntity, update_on_db: bool = False
    ) -> PurchaseLineEntity:
        sri_config = self.site_repository.get_sri_config()
        purchaseline_entity = self.calculate_purchaseline_total_usecase.execute(
            purchaseline_entity, sri_config
        )

        if update_on_db:
            self.purchaseline_repository.save(
                purchaseline_entity, update_fields=["subtotal", "tax", "total"]
            )

        return purchaseline_entity
