from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

submenu_items = [
    MenuItem(
        _("categories").capitalize(),
        reverse("packs:warehouses_productcategory_list"),
        weight=10,
        icon="bx-right-arrow-alt",
    ),
    MenuItem(
        _("measures").capitalize(),
        reverse("packs:warehouses_measure_list"),
        weight=11,
        icon="bx-right-arrow-alt",
    ),
    MenuItem(
        _("products").capitalize(),
        reverse("packs:warehouses_product_list"),
        weight=12,
        icon="bx-right-arrow-alt",
    ),
]

warehouses_item = MenuItem(
    _("warehouses").capitalize(), "#", icon="bxs-store", children=submenu_items
)
