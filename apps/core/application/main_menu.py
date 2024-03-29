from dependency_injector.wiring import Provide, inject
from django.utils.translation import gettext_lazy as _
from simple_menu import Menu, MenuItem

from apps.core.domain.repositories import MenuRepository
from apps.core.menu.inventories import inventories_item
from apps.core.menu.sales import sales_item


@inject
def build_main_menu(
    menu_service: MenuRepository = Provide["core_package.menu_service"],
):
    submenu_items = [
        inventories_item,
        sales_item,
        menu_service.retrieve_menu_item(),
    ]
    Menu.add_item(
        "main",
        MenuItem(_("modules"), "", children=submenu_items),
    )
