from django.utils.translation import gettext_lazy as _
from simple_menu import Menu, MenuItem

from .config import config_item
from .sales import sales_item
from .warehouses import warehouses_item

submenu_items = [warehouses_item, sales_item, config_item]

Menu.add_item(
    "main",
    MenuItem(_("modules"), "", children=submenu_items),
)
