from typing import List

from apps.sale.domain.entities import VoucherTypeEntity
from apps.sale.domain.repositories import VoucherTypeRepository

from .ports import GenerateVoucherTypeSequencePort


class GenerateVoucherTypeSequenceUseCase(GenerateVoucherTypeSequencePort):
    def __init__(self, voucher_type_repository: VoucherTypeRepository) -> None:
        self.sequence_length = 9
        self.voucher_type_repository = voucher_type_repository

    def generate_sequence(self, voucher_code: str) -> str:
        sequence = 1
        voucher_type = self.filter_by_code(code=voucher_code)

        if voucher_type:
            sequence = voucher_type.current + 1
            voucher_type.current = sequence
            self.save(voucher_type, update_fields=["current"])

        return str(sequence).zfill(self.sequence_length)

    def filter_by_code(self, voucher_code: str) -> VoucherTypeEntity:
        return self.voucher_type_repository.filter_by_code(voucher_code)

    def save(
        self, voucher_type: VoucherTypeEntity, update_fields: List[str] = None
    ) -> None:
        self.save(voucher_type, update_fields)
