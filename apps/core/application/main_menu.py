from dependency_injector.wiring import Provide, inject
from django.utils.translation import gettext_lazy as _
from simple_menu import Menu, MenuItem

from apps.core.domain.repositories import MenuRepository


@inject
def build_main_menu(
    core_menu_repository: MenuRepository = Provide["core_package.menu_repository"],
    inventory_menu_repository: MenuRepository = Provide[
        "inventory_package.menu_repository"
    ],
    purchase_menu_repository: MenuRepository = Provide[
        "purchase_package.menu_repository"
    ],
    sale_menu_repository: MenuRepository = Provide["sale_package.menu_repository"],
):
    submenu_items = [
        inventory_menu_repository.retrieve_menu_item(),
        purchase_menu_repository.retrieve_menu_item(),
        sale_menu_repository.retrieve_menu_item(),
        core_menu_repository.retrieve_menu_item(),
    ]
    Menu.add_item(
        "main",
        MenuItem(_("modules"), "", children=submenu_items),
    )
