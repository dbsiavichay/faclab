from datetime import datetime
from typing import Any, Dict, List

import pytz
import xmltodict
from django.conf import settings

from apps.core.domain.entities import SRIConfig
from apps.sale.domain.entities import CustomerEntity
from apps.sri.domain.entities import (
    InvoiceDetailInfo,
    InvoiceInfo,
    PaymentInfo,
    TaxInfo,
    VoucherEntity,
)
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

    def execute(self, access_code: str) -> VoucherEntity:
        return self.sri_voucher_port.retrieve_voucher_by_access_code(access_code)


class GenerateVoucherXmlUseCase:
    def get_invoice_data(
        self,
        customer: CustomerEntity,
        tax_info: TaxInfo,
        invoice_info: InvoiceInfo,
        details: List[InvoiceDetailInfo],
        payments: List[PaymentInfo],
    ) -> Dict[str, Any]:
        data = {
            "factura": {
                "@id": "comprobante",
                "@version": "1.0.0",
                "infoTributaria": tax_info.model_dump(by_alias=True),
                "infoFactura": {
                    **invoice_info.model_dump(exclude_none=True, by_alias=True),
                    "pagos": {"pago": []},
                },
                "detalles": {"detalle": []},
                "infoAdicional": {"campoAdicional": []},
            }
        }

        if customer.address:
            data["factura"]["infoAdicional"]["campoAdicional"].append(
                {"@nombre": "Dirección", "#text": customer.address}
            )

        if customer.phone:
            data["factura"]["infoAdicional"]["campoAdicional"].append(
                {"@nombre": "Telefono", "#text": customer.phone}
            )

        data["factura"]["infoAdicional"]["campoAdicional"].append(
            {"@nombre": "Email", "#text": customer.email}
        )

        for payment in payments:
            data["factura"]["infoFactura"]["pagos"]["pago"].append(
                payment.model_dump(by_alias=True)
            )

        for detail in details:
            data["factura"]["detalles"]["detalle"].append(
                detail.model_dump(by_alias=True)
            )

        return data

    def execute(
        self,
        customer: CustomerEntity,
        tax_info: TaxInfo,
        invoice_info: InvoiceInfo,
        details: List[InvoiceDetailInfo],
        payments: List[PaymentInfo],
    ) -> str:
        data = self.get_invoice_data(
            customer, tax_info, invoice_info, details, payments
        )
        xml = xmltodict.unparse(data, pretty=True)

        return xml


"""
class InvoiceServiceLegacy:
    INVOICE_CODE = "01"

    @classmethod
    def sign_xml(cls, invoice):
        signer = SRISigner()
        str_signed_invoice = signer.sign(invoice.file.read())
        xml_file = NamedTemporaryFile(suffix=".xml")

        with open(xml_file.name, "w") as file:
            file.write(str_signed_invoice)

        file.close()
        file_name = f"{invoice.code}.xml"
        content_file = ContentFile(xml_file.read())
        file = File(file=content_file, name=file_name)
        invoice.file.delete()
        invoice.file = file
        invoice.status = VoucherStatuses.SIGNED
        invoice.save(update_fields=["status", "file"])

        return file

    @classmethod
    def send_xml(cls, invoice):
        client = SRIClient()
        client.send_voucher(invoice.file.read())
        _, authotization_date = client.fetch_voucher(invoice.code)
        invoice.authorization_date = authotization_date
        invoice.status = VoucherStatuses.AUTHORIZED
        invoice.save(update_fields=["authorization_date", "status"])
"""
