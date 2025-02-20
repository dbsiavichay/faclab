from datetime import datetime
from typing import List

from dependency_injector.wiring import Provide, inject

from apps.core.domain.repositories import SiteRepository
from apps.sale.domain.entities import CustomerEntity
from apps.sri.application.usecases import (
    GenerateVoucherAccessCodeUseCase,
    GenerateVoucherXmlUseCase,
    RetrieveVoucherXmlUseCase,
    SendVoucherXmlUseCase,
)
from apps.sri.domain.entities import (
    AuthorizationResult,
    InvoiceDetailInfo,
    InvoiceInfo,
    PaymentInfo,
    TaxInfo,
)


class SRIVoucherService:
    @inject
    def __init__(
        self,
        generate_access_code_usecase: GenerateVoucherAccessCodeUseCase,
        generate_voucher_xml_usecase: GenerateVoucherXmlUseCase,
        send_voucher_xml_usecase: SendVoucherXmlUseCase,
        retrieve_voucher_xml_usecase: RetrieveVoucherXmlUseCase,
        site_repository: SiteRepository = Provide["core_package.site_repository"],
    ) -> None:
        self.generate_access_code_usecase = generate_access_code_usecase
        self.generate_voucher_xml_usecase = generate_voucher_xml_usecase
        self.send_voucher_xml_usecase = send_voucher_xml_usecase
        self.retrieve_voucher_xml_usecase = retrieve_voucher_xml_usecase
        self.site_repository = site_repository

    def generate_access_code(
        self,
        voucher_type_code: str,
        voucher_id: int,
        voucher_date: datetime,
        voucher_sequence: str,
    ) -> str:
        sri_config = self.site_repository.get_sri_config()
        return self.generate_access_code_usecase.execute(
            voucher_type_code, voucher_id, voucher_date, voucher_sequence, sri_config
        )

    def generate_voucher_xml(
        self,
        customer: CustomerEntity,
        tax_info: TaxInfo,
        invoice_info: InvoiceInfo,
        details: List[InvoiceDetailInfo],
        payments: List[PaymentInfo],
    ) -> str:
        return self.generate_voucher_xml_usecase.execute(
            customer, tax_info, invoice_info, details, payments
        )

    def send_voucher_xml(self, voucher: bytes) -> bool:
        return self.send_voucher_xml_usecase.execute(voucher)

    def retrieve_voucher_xml(self, access_code: str) -> AuthorizationResult:
        return self.retrieve_voucher_xml_usecase.execute(access_code)
