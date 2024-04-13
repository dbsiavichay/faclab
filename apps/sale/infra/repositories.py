from tempfile import NamedTemporaryFile
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
from apps.sale.models import Invoice, InvoiceLine, VoucherType


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
    def upload_xml(self, invoice_entity: InvoiceEntity, xml: str):
        invoice = Invoice(id=invoice_entity.id)
        invoice.refresh_from_db()
        xml_file = NamedTemporaryFile(suffix=".xml")

        with open(xml_file.name, "w") as file:
            file.write(xml)

        file.close()

        invoice.file.delete()
        file_name = f"{invoice_entity.access_code}.xml"
        content_file = ContentFile(xml_file.read())
        file = File(file=content_file, name=file_name)
        invoice.file = file
        invoice.save(update_fields=["file"])

    def save(
        self, invoice_entity: InvoiceEntity, update_fields: List[str] = None
    ) -> None:
        invoice = Invoice(**invoice_entity.model_dump())
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
