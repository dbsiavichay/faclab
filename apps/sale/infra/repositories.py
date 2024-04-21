from typing import List, Optional

from django.core.files import File
from django.core.files.base import ContentFile
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from apps.core.domain.repositories import MenuRepository
from apps.sale.domain.entities import (
    InvoiceEntity,
    InvoiceLineEntity,
    VoucherTypeEntity,
)
from apps.sale.domain.repositories import (
    InvoiceLineRepository,
    InvoiceRepository,
    VoucherTypeRepository,
)

from .models import Invoice, InvoiceLine, VoucherType


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


class InvoiceLineRepositoryImpl(InvoiceLineRepository):
    def get_consolidated_lines_subtotal(self, invoice_id: int) -> float:
        subtotal = (
            InvoiceLine.objects.filter(invoice_id=invoice_id)
            .aggregate(subtotal=Sum("subtotal"))
            .get("subtotal")
        )
        return subtotal

    def save(
        self, invoiceline_entity: InvoiceLineEntity, update_fields: List[str] = None
    ) -> None:
        invoiceline = InvoiceLine(**invoiceline_entity.model_dump())
        invoiceline.save(update_fields=update_fields)


class InvoiceRepositoryImpl(InvoiceRepository):
    def upload_xml(self, invoice_entity: InvoiceEntity):
        invoice = Invoice(id=invoice_entity.id)
        invoice.refresh_from_db()
        invoice.file.delete()
        file_name = f"{invoice_entity.access_code}.xml"
        content_file = ContentFile(invoice_entity.xml_bytes)
        file = File(file=content_file, name=file_name)
        invoice.file = file
        invoice.save(update_fields=["file"])

    def find_by_id(self, id: int) -> Optional[InvoiceEntity]:
        invoice = Invoice.objects.filter(id=id).first()

        if invoice:
            return InvoiceEntity(xml_bytes=invoice.file.read(), **invoice.__dict__)

        return None

    def find_by_id_with_related(self, id: int) -> Optional[InvoiceEntity]:
        invoice = (
            Invoice.objects.prefetch_related("customer__code_type", "lines", "payments")
            .filter(id=id)
            .first()
        )

        if not invoice:
            return None

        customer = {
            "code_type_code": invoice.customer.code_type.code,
            **invoice.customer.__dict__,
        }

        invoice_lines = [line.__dict__ for line in invoice.lines.all()]
        invoice_payments = [payment.__dict__ for payment in invoice.payments.all()]

        invoice_entity = InvoiceEntity(
            customer=customer,
            lines=invoice_lines,
            payments=invoice_payments,
            **invoice.__dict__,
        )

        if invoice.file:
            invoice_entity.xml_bytes = invoice.file.read()

        return invoice_entity

    def save(
        self, invoice_entity: InvoiceEntity, update_fields: List[str] = None
    ) -> None:
        exclude_fields = ["customer", "lines", "payments", "xml_str", "xml_bytes"]
        invoice = Invoice(
            **invoice_entity.model_dump(exclude=exclude_fields),
        )
        invoice.save(update_fields=update_fields)


class MenuRepositoryImpl(MenuRepository):
    def retrieve_menu_item(self) -> MenuItem:
        submenu_items = self.retrieve_menu_items()

        return MenuItem(
            _("sales").capitalize(),
            "#",
            icon="bxs-shopping-bag",
            children=submenu_items,
        )

    def retrieve_menu_items(self) -> List[MenuItem]:
        return [
            MenuItem(
                _("customers").capitalize(),
                reverse("packs:sale_customer_list"),
                weight=20,
                icon="bx-right-arrow-alt",
            ),
            MenuItem(
                _("invoices").capitalize(),
                reverse("packs:sale_invoice_list"),
                weight=20,
                icon="bx-right-arrow-alt",
            ),
        ]
