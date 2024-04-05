from abc import ABC, abstractmethod
from typing import List, Optional

from apps.sale.domain.entities import VoucherTypeEntity


class GenerateVoucherSequencePort(ABC):
    @abstractmethod
    def generate_sequence(self, voucher_type_code: str) -> str:
        pass

    @abstractmethod
    def find_voucher_type_by_code(
        self, voucher_type_code: str
    ) -> Optional[VoucherTypeEntity]:
        pass

    @abstractmethod
    def save_voucher_type(
        self, voucher_type_entity: VoucherTypeEntity, update_fields: List[str] = None
    ) -> None:
        pass


class GenerateInvoiceAccessCodePort(ABC):
    @abstractmethod
    def generate_access_code(self, voucher_type_code: str) -> str:
        pass
