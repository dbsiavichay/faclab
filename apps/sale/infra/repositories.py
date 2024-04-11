from typing import List, Optional

from apps.sale.domain.entities import InvoiceEntity, VoucherTypeEntity
from apps.sale.domain.repositories import InvoiceRepository, VoucherTypeRepository
from apps.sale.models import Invoice, VoucherType


class VoucherTypeRepositoryImpl(VoucherTypeRepository):
    def find_by_code(self, code: str) -> Optional[VoucherTypeEntity]:
        voucher_type = VoucherType.objects.values().filter(code=code).first()

        if voucher_type:
            return VoucherTypeEntity(**voucher_type)

        return voucher_type

    def save(
        self, voucher_type_entity: VoucherTypeEntity, update_fields: List[str] = None
    ) -> None:
        voucher_type = VoucherType(**voucher_type_entity.model_dump())
        voucher_type.save(update_fields=update_fields)


class InvoiceRepositoryImpl(InvoiceRepository):
    def save(
        self, invoice_entity: InvoiceEntity, update_fields: List[str] = None
    ) -> None:
        invoice = Invoice(**invoice_entity.model_dump())
        invoice.save(update_fields=update_fields)
