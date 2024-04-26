from typing import List

from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from apps.core.domain.repositories import MenuRepository
from apps.inventory.domain.entities import PurchaseEntity, PurchaseLineEntity
from apps.inventory.domain.repositories import (
    PurchaseLineRepository,
    PurchaseRepository,
)
from apps.inventory.infra.models import Purchase, PurchaseLine


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
            _("inventory").capitalize(), "#", icon="bxs-store", children=submenu_items
        )

    def retrieve_menu_items(self) -> List[MenuItem]:
        return [
            MenuItem(
                _("providers").capitalize(),
                reverse("packs:inventory_provider_list"),
                weight=10,
                icon="bx-right-arrow-alt",
            ),
            MenuItem(
                _("categories").capitalize(),
                reverse("packs:inventory_productcategory_list"),
                weight=11,
                icon="bx-right-arrow-alt",
            ),
            MenuItem(
                _("measures").capitalize(),
                reverse("packs:inventory_measure_list"),
                weight=12,
                icon="bx-right-arrow-alt",
            ),
            MenuItem(
                _("products").capitalize(),
                reverse("packs:inventory_product_list"),
                weight=13,
                icon="bx-right-arrow-alt",
            ),
            MenuItem(
                _("purchases").capitalize(),
                reverse("packs:inventory_purchase_list"),
                weight=14,
                icon="bx-right-arrow-alt",
            ),
        ]
