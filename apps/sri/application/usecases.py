from datetime import datetime

import pytz
from django.conf import settings

from apps.core.domain.entities import SRIConfig
from apps.sri.domain.entities import VoucherEntity
from apps.sri.domain.ports import SRIVoucherPort


class GenerateVoucherAccessCodeUseCase:
    def __init__(self) -> None:
        self.date_format_code = "%d%m%Y"
        self.voucher_number_length = 8

    def execute(
        self,
        voucher_type_code: str,
        voucher_id: int,
        voucher_date: datetime,
        voucher_sequence: str,
        sri_config: SRIConfig,
    ) -> str:
        timezone = pytz.timezone(settings.TIME_ZONE)
        voucher_date = voucher_date.astimezone(timezone)
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


class RetrieveVoucherUseCase:
    def __init__(self, sri_voucher_port: SRIVoucherPort) -> None:
        self.sri_voucher_port = sri_voucher_port

    def execute(self, code: str) -> VoucherEntity:
        return self.sri_voucher_port.retrieve_voucher_by_code(code)
