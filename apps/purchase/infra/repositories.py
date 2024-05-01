from typing import List

from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from apps.core.domain.repositories import MenuRepository
from apps.purchase.domain.entities import PurchaseEntity, PurchaseLineEntity
from apps.purchase.domain.repositories import PurchaseLineRepository, PurchaseRepository
from apps.purchase.infra.models import Purchase, PurchaseLine


class PurchaseRepositoryImpl(PurchaseRepository):
    def get_consolidated_subtotal(self, purchase_entity: PurchaseEntity) -> float:
        purchase = Purchase(id=purchase_entity.id)
        subtotal = purchase.lines.aggregate(subtotal=Sum("subtotal")).get("subtotal")

        return subtotal

    def save(
        self, purchase_entity: PurchaseEntity, update_fields: List[str] = None
    ) -> None:
        purchase = Purchase(**purchase_entity.model_dump())
        purchase.save(update_fields=update_fields)


class PurchaseLineRepositoryImpl(PurchaseLineRepository):
    def save(
        self, purchaseline_entity: PurchaseLineEntity, update_fields: List[str] = None
    ) -> None:
        invoiceline = PurchaseLine(**purchaseline_entity.model_dump())
        invoiceline.save(update_fields=update_fields)


class MenuRepositoryImpl(MenuRepository):
    def retrieve_menu_item(self) -> MenuItem:
        submenu_items = self.retrieve_menu_items()

        return MenuItem(
            _("purchases").capitalize(), "#", icon="bxs-basket", children=submenu_items
        )

    def retrieve_menu_items(self) -> List[MenuItem]:
        return [
            MenuItem(
                _("providers").capitalize(),
                reverse("packs:purchase_provider_list"),
                weight=10,
                icon="bx-right-arrow-alt",
            ),
            MenuItem(
                _("invoices").capitalize(),
                reverse("packs:purchase_purchase_list"),
                weight=14,
                icon="bx-right-arrow-alt",
            ),
        ]
