from tempfile import NamedTemporaryFile

from dependency_injector.wiring import Provide, inject

from apps.core.application.services import SealifyService
from apps.core.domain.repositories import SiteRepository
from apps.sale.application.usecases import (
    CalculateInvoiceTotalUseCase,
    GenerateVoucherSequenceUseCase,
)
from apps.sale.domain.entities import InvoiceEntity, InvoiceLineEntity
from apps.sale.domain.enums import VoucherStatusEnum
from apps.sale.domain.repositories import InvoiceLineRepository, InvoiceRepository
from apps.sri.application.services import SRIVoucherService
from apps.sri.domain.entities import (
    InvoiceDetailInfo,
    InvoiceInfo,
    PaymentInfo,
    TaxInfo,
    TaxValueInfo,
)


class InvoiceService:
    @inject
    def __init__(
        self,
        invoice_repository: InvoiceRepository,
        invoiceline_repository: InvoiceLineRepository,
        generate_voucher_sequence_usecase: GenerateVoucherSequenceUseCase,
        calculate_invoice_total_usecase: CalculateInvoiceTotalUseCase,
        sri_voucher_service: SRIVoucherService,
        sealify_service: SealifyService = Provide["core_package.sealify_service"],
        site_repository: SiteRepository = Provide["core_package.site_repository"],
    ) -> None:
        self.invoice_voucher_type_code = "01"
        self.invoice_repository = invoice_repository
        self.invoiceline_repository = invoiceline_repository
        self.generate_voucher_sequence_usecase = generate_voucher_sequence_usecase
        self.calculate_invoice_total_usecase = calculate_invoice_total_usecase
        self.sri_voucher_service = sri_voucher_service
        self.sealify_service = sealify_service
        self.site_repository = site_repository

    def update_invoice_sequence(
        self, invoice_entity: InvoiceEntity, update_on_db: bool = False
    ) -> str:
        invoice_entity.sequence = self.generate_voucher_sequence_usecase.execute(
            self.invoice_voucher_type_code
        )

        if update_on_db:
            self.invoice_repository.save(invoice_entity, update_fields=["sequence"])

        return invoice_entity

    def update_invoice_access_code(
        self, invoice_entity: InvoiceEntity, update_on_db: bool = False
    ) -> InvoiceEntity:
        invoice_entity.access_code = self.sri_voucher_service.generate_access_code(
            self.invoice_voucher_type_code,
            invoice_entity.id,
            invoice_entity.date,
            invoice_entity.sequence,
        )

        if update_on_db:
            self.invoice_repository.save(invoice_entity, update_fields=["access_code"])

        return invoice_entity

    def update_invoice_line_total(
        self, invoiceline_entity: InvoiceLineEntity, update_on_db: bool = False
    ) -> InvoiceLineEntity:
        sri_config = self.site_repository.get_sri_config()
        invoiceline_entity = (
            self.calculate_invoice_total_usecase.execute_by_invoiceline(
                invoiceline_entity, sri_config
            )
        )

        if update_on_db:
            self.invoiceline_repository.save(
                invoiceline_entity, update_fields=["subtotal", "tax", "total"]
            )

        return invoiceline_entity

    def update_invoice_total(
        self, invoice_entity: InvoiceEntity, update_on_db: bool = False
    ) -> InvoiceEntity:
        sri_config = self.site_repository.get_sri_config()
        invoice_entity = self.calculate_invoice_total_usecase.execute_by_invoice(
            invoice_entity, sri_config
        )

        if update_on_db:
            self.invoice_repository.save(
                invoice_entity, update_fields=["subtotal", "tax", "total"]
            )

        return invoice_entity

    def update_invoice_xml(
        self, invoice_entity: InvoiceEntity, update_on_db: bool = False
    ):
        sri_config = self.site_repository.get_sri_config()
        tax_info_dict = {**sri_config.model_dump(), **invoice_entity.model_dump()}
        tax_info = TaxInfo(**tax_info_dict)
        invoice_taxes = [
            TaxValueInfo(
                code=2,
                percentage_code=4,
                base=invoice_entity.subtotal,
                value=invoice_entity.tax,
            )
        ]
        invoice_info_dict = {
            **invoice_entity.customer.model_dump(),
            **invoice_entity.model_dump(),
            **sri_config.model_dump(),
        }
        invoice_info = InvoiceInfo(
            **invoice_info_dict,
            voucher_taxes=invoice_taxes,
        )
        details_invoice = [
            InvoiceDetailInfo(
                main_code="prod",
                aux_code="prod",
                description="producto",
                quantity=line.quantity,
                unit_price=line.unit_price,
                subtotal=line.subtotal,
                taxes=[
                    TaxValueInfo(
                        code=2,
                        percentage_code=4,
                        fee=15,
                        base=line.subtotal,
                        value=line.tax,
                    )
                ],
            )
            for line in invoice_entity.lines
        ]

        payments = [
            PaymentInfo(**payment.model_dump()) for payment in invoice_entity.payments
        ]

        xml = self.sri_voucher_service.generate_voucher_xml(
            invoice_entity.customer, tax_info, invoice_info, details_invoice, payments
        )
        xml_file = NamedTemporaryFile(suffix=".xml")

        with open(xml_file.name, "w") as file:
            file.write(xml)

        file.close()

        invoice_entity.xml_str = xml
        invoice_entity.xml_bytes = xml_file.read()

        if update_on_db:
            self.invoice_repository.upload_xml(invoice_entity)

        return invoice_entity

    def seal_invoice_xml(
        self, invoice_entity: InvoiceEntity, update_on_db: bool = False
    ):
        config = self.site_repository.get_sri_config()
        certificate_id = config.signature
        sealed_invoice = self.sealify_service.seal_invoice(
            invoice_entity.xml_str, certificate_id
        )
        xml = sealed_invoice.sealed_data
        xml_file = NamedTemporaryFile(suffix=".xml")

        with open(xml_file.name, "w") as file:
            file.write(xml)

        file.close()

        invoice_entity.xml_str = xml
        invoice_entity.xml_bytes = xml_file.read()
        invoice_entity.status = VoucherStatusEnum.SIGNED

        if update_on_db:
            self.invoice_repository.upload_xml(invoice_entity)
            self.invoice_repository.save(invoice_entity, update_fields=["status"])

        return invoice_entity

    def send_invoice_xml(
        self, invoice_entity: InvoiceEntity, update_on_db: bool = False
    ):
        self.sri_voucher_service.send_voucher_xml(invoice_entity.xml_bytes)
        result = self.sri_voucher_service.retrieve_voucher_xml(
            invoice_entity.access_code
        )
        invoice_entity.authorization_date = result.authorization_date
        invoice_entity.status = VoucherStatusEnum.AUTHORIZED

        if update_on_db:
            self.invoice_repository.save(
                invoice_entity, update_fields=["authorization_date", "status"]
            )

    def build_invoice_entity(self, invoice_id: int) -> InvoiceEntity:
        return self.invoice_repository.find_by_id_with_related(invoice_id)
