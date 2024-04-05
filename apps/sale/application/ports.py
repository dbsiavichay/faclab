from abc import ABC, abstractmethod
from typing import List, Optional

from apps.sale.domain.entities import VoucherTypeEntity


class GenerateVoucherTypeSequencePort(ABC):
    @abstractmethod
    def generate_sequence(self, voucher_code: str) -> str:
        pass

    @abstractmethod
    def filter_by_code(self, voucher_code: str) -> Optional[VoucherTypeEntity]:
        pass

    @abstractmethod
    def save(
        self, voucher_type: VoucherTypeEntity, update_fields: List[str] = None
    ) -> None:
        pass
