from typing import List, Optional

from apps.core.domain.entities import SRIConfig
from apps.sale.domain.entities import (
    InvoiceEntity,
    InvoiceLineEntity,
    VoucherTypeEntity,
)
from apps.sale.domain.repositories import InvoiceLineRepository, VoucherTypeRepository


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


class CalculateInvoiceTotalUseCase:
    def __init__(self, invoiceline_repository: InvoiceLineRepository) -> None:
        self.invoiceline_repository = invoiceline_repository

    def execute_by_invoiceline(
        self, invoiceline_entity: InvoiceLineEntity, sri_config: SRIConfig
    ) -> InvoiceLineEntity:
        invoiceline_entity.subtotal = (
            invoiceline_entity.unit_price * invoiceline_entity.quantity
        )
        invoiceline_entity.tax = invoiceline_entity.subtotal * sri_config.iva_rate
        invoiceline_entity.total = invoiceline_entity.subtotal * sri_config.iva_factor

        return invoiceline_entity

    def execute_by_invoice(
        self, invoice_entity: InvoiceEntity, sri_config: SRIConfig
    ) -> InvoiceEntity:
        subtotal = self.invoiceline_repository.get_consolidated_lines_subtotal(
            invoice_entity.id
        )
        invoice_entity.subtotal = subtotal
        invoice_entity.tax = subtotal * sri_config.iva_rate
        invoice_entity.total = subtotal * sri_config.iva_factor

        return invoice_entity
