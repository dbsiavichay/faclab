from abc import ABC, abstractmethod
from typing import List, Optional

from apps.sale.domain.entities import VoucherTypeEntity


class VoucherTypeRepository(ABC):
    @abstractmethod
    def find_by_code(self, code: str) -> Optional[VoucherTypeEntity]:
        pass

    @abstractmethod
    def save(
        self, voucher_type: VoucherTypeEntity, update_fields: List[str] = None
    ) -> None:
        pass
