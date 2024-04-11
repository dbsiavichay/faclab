from typing import List, Optional

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from apps.core.domain.repositories import MenuRepository
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
