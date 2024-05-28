from abc import ABC, abstractmethod
from typing import List, Optional

from apps.sale.domain.entities import (
    InvoiceEntity,
    InvoiceLineEntity,
    VoucherTypeEntity,
)


class VoucherTypeRepository(ABC):
    @abstractmethod
    def find_by_code(self, code: str) -> Optional[VoucherTypeEntity]:
        pass

    @abstractmethod
    def save(
        self, voucher_type_entity: VoucherTypeEntity, update_fields: List[str] = None
    ) -> None:
        pass


class InvoiceLineRepository(ABC):
    @abstractmethod
    def get_consolidated_lines_subtotal(self, invoice_id: int) -> float:
        pass

    @abstractmethod
    def save(
        self, invoiceline_entity: InvoiceLineEntity, update_fields: List[str] = None
    ) -> None:
        pass


class InvoiceRepository(ABC):
    @abstractmethod
    def upload_xml(self, invoice_entity: InvoiceEntity):
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[InvoiceEntity]:
        pass

    @abstractmethod
    def find_by_id_with_related(self, id: int) -> Optional[InvoiceEntity]:
        pass

    @abstractmethod
    def save(
        self, invoice_entity: InvoiceEntity, update_fields: List[str] = None
    ) -> None:
        pass
