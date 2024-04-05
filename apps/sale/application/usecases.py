import datetime
from typing import List, Optional

import pytz
from django.conf import settings

from apps.core.domain.entities import SRIConfig
from apps.sale.domain.entities import VoucherTypeEntity
from apps.sale.domain.repositories import VoucherTypeRepository

from .ports import GenerateInvoiceAccessCodePort, GenerateVoucherSequencePort


class GenerateVoucherSequenceUseCase(GenerateVoucherSequencePort):
    def __init__(self, voucher_type_repository: VoucherTypeRepository) -> None:
        self.sequence_length = 9
        self.voucher_type_repository = voucher_type_repository

    def generate_sequence(self, voucher_type_code: str) -> str:
        sequence = 1
        voucher_type = self.find_voucher_type_by_code(
            voucher_type_code=voucher_type_code
        )

        if voucher_type:
            sequence = voucher_type.current + 1
            voucher_type.current = sequence
            self.save_voucher_type(voucher_type, update_fields=["current"])

        return str(sequence).zfill(self.sequence_length)

    def find_voucher_type_by_code(
        self, voucher_type_code: str
    ) -> Optional[VoucherTypeEntity]:
        return self.voucher_type_repository.find_by_code(voucher_type_code)

    def save_voucher_type(
        self, voucher_type_entity: VoucherTypeEntity, update_fields: List[str] = None
    ) -> None:
        self.voucher_type_repository.save(voucher_type_entity, update_fields)


class GenerateInvoiceAccessCodeUseCase(GenerateInvoiceAccessCodePort):
    def __init__(self) -> None:
        self.date_format_code = "%d%m%Y"
        self.voucher_number_length = 8

    def generate_access_code(
        self,
        sri_config: SRIConfig,
        voucher_type_code: str,
        voucher_id: int,
        voucher_date: datetime,
        voucher_sequence: str,
    ) -> str:
        timezone = pytz.timezone(settings.TIME_ZONE)
        voucher_date = voucher_date.issue_date.astimezone(timezone)
        voucher_date_str = voucher_date.strftime(self.date_format_code)
        voucher_serie = f"{sri_config.company_code}{sri_config.company_point_sale_code}"
        voucher_number = str(voucher_id)[: self.voucher_number_length].zfill(
            self.voucher_number_length
        )
        code = "{0}{1}{2}{3}{4}{5}{6}{7}".format(
            voucher_date_str,
            voucher_type_code,
            sri_config.code,
            sri_config.environment,
            voucher_serie,
            voucher_sequence,
            voucher_number,
            sri_config.emission,
        )
        factor = 2
        sum = 0
        reversed_code = code[::-1]

        for char in reversed_code:
            number = int(char)
            number = number * factor
            sum = sum + number
            factor = factor + 1
            factor = 2 if factor > 7 else factor

        verifier = 11 - (sum % 11)
        verifier = 0 if verifier == 11 else 1 if verifier == 10 else verifier
        code = f"{code}{verifier}"

        return code
