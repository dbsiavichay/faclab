from typing import List, Optional

from apps.sale.domain.entities import VoucherTypeEntity
from apps.sale.domain.repositories import VoucherTypeRepository


class GenerateVoucherSequenceUseCase:
    def __init__(self, voucher_type_repository: VoucherTypeRepository) -> None:
        self.sequence_length = 9
        self.voucher_type_repository = voucher_type_repository

    def find_voucher_type_by_code(
        self, voucher_type_code: str
    ) -> Optional[VoucherTypeEntity]:
        return self.voucher_type_repository.find_by_code(voucher_type_code)

    def save_voucher_type(
        self, voucher_type_entity: VoucherTypeEntity, update_fields: List[str] = None
    ) -> None:
        self.voucher_type_repository.save(voucher_type_entity, update_fields)

    def execute(self, voucher_type_code: str) -> str:
        sequence = 1
        voucher_type = self.find_voucher_type_by_code(
            voucher_type_code=voucher_type_code
        )

        if voucher_type:
            sequence = voucher_type.current + 1
            voucher_type.current = sequence
            self.save_voucher_type(voucher_type, update_fields=["current"])

        return str(sequence).zfill(self.sequence_length)
