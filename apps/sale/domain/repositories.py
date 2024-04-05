from abc import ABC, abstractmethod
from typing import List, Optional

from apps.sale.domain.entities import InvoiceEntity, VoucherTypeEntity


class VoucherTypeRepository(ABC):
    @abstractmethod
    def find_by_code(self, code: str) -> Optional[VoucherTypeEntity]:
        pass

    @abstractmethod
    def save(
        self, voucher_type: VoucherTypeEntity, update_fields: List[str] = None
    ) -> None:
        pass


class InvoiceRepository(ABC):
    @abstractmethod
    def save(
        self, invoice_entity: InvoiceEntity, update_fields: List[str] = None
    ) -> None:
        pass
