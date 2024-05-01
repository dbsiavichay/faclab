from apps.core.domain.entities import SRIConfig
from apps.purchase.domain.entities import PurchaseEntity, PurchaseLineEntity
from apps.purchase.domain.repositories import PurchaseRepository


class CalculatePurchaseLineTotalUseCase:
    def execute(
        self, purchaseline_entity: PurchaseLineEntity, sri_config: SRIConfig
    ) -> PurchaseLineEntity:
        purchaseline_entity.subtotal = (
            purchaseline_entity.unit_price * purchaseline_entity.quantity
        )
        purchaseline_entity.tax = purchaseline_entity.subtotal * sri_config.iva_rate
        purchaseline_entity.total = purchaseline_entity.subtotal * sri_config.iva_factor

        return purchaseline_entity


class CalculatePurchaseTotalUseCase:
    def __init__(self, purchase_repository: PurchaseRepository) -> None:
        self.purchase_repository = purchase_repository

    def execute(
        self, purchase_entity: PurchaseEntity, sri_config: SRIConfig
    ) -> PurchaseEntity:
        subtotal = self.purchase_repository.get_consolidated_subtotal(purchase_entity)
        purchase_entity.subtotal = subtotal
        purchase_entity.tax = subtotal * sri_config.iva_rate
        purchase_entity.total = subtotal * sri_config.iva_factor

        return purchase_entity
