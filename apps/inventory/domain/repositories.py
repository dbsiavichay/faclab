from abc import ABC, abstractmethod
from typing import List

from apps.inventory.domain.entities import PurchaseEntity, PurchaseLineEntity


class PurchaseRepository(ABC):
    @abstractmethod
    def get_consolidated_subtotal(self, purchase_entity: PurchaseEntity) -> float:
        pass

    def save(
        self, purchase_entity: PurchaseEntity, update_fields: List[str] = None
    ) -> None:
        pass


class PurchaseLineRepository(ABC):
    @abstractmethod
    def save(
        self, purchaseline_entity: PurchaseLineEntity, update_fields: List[str] = None
    ) -> None:
        pass
