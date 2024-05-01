from typing import List

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from apps.core.domain.repositories import MenuRepository


class MenuRepositoryImpl(MenuRepository):
    def retrieve_menu_item(self) -> MenuItem:
        submenu_items = self.retrieve_menu_items()

        return MenuItem(
            _("inventory").capitalize(), "#", icon="bxs-store", children=submenu_items
        )

    def retrieve_menu_items(self) -> List[MenuItem]:
        return [
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
        ]
