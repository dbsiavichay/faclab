from datetime import datetime
from typing import List

from dependency_injector.wiring import Provide, inject

from apps.core.domain.repositories import SignatureRepository, SiteRepository
from apps.sale.domain.entities import CustomerEntity
from apps.sri.application.usecases import (
    GenerateVoucherAccessCodeUseCase,
    GenerateVoucherXmlUseCase,
    RetrieveVoucherXmlUseCase,
    SendVoucherXmlUseCase,
    SignVoucherXmlUseCase,
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
        sign_voucher_xml_usecase: SignVoucherXmlUseCase,
        send_voucher_xml_usecase: SendVoucherXmlUseCase,
        retrieve_voucher_xml_usecase: RetrieveVoucherXmlUseCase,
        site_repository: SiteRepository = Provide["core_package.site_repository"],
        signature_repository: SignatureRepository = Provide[
            "core_package.signature_repository"
        ],
    ) -> None:
        self.signature_repository = signature_repository
        self.generate_access_code_usecase = generate_access_code_usecase
        self.generate_voucher_xml_usecase = generate_voucher_xml_usecase
        self.sign_voucher_xml_usecase = sign_voucher_xml_usecase
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

    def sign_voucher_xml(self, voucher: bytes):
        config = self.site_repository.get_sri_config()
        # TODO: Validar que exista la configuracion y modelo
        signature_id = config.signature
        signature = self.signature_repository.find_by_id(signature_id)

        return self.sign_voucher_xml_usecase.execute(
            voucher, signature.cert, signature.key
        )

    def send_voucher_xml(self, voucher: bytes) -> bool:
        return self.send_voucher_xml_usecase.execute(voucher)

    def retrieve_voucher_xml(self, access_code: str) -> AuthorizationResult:
        return self.retrieve_voucher_xml_usecase.execute(access_code)
