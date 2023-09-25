from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

submenu_items = [
    MenuItem(
        _("providers").capitalize(),
        reverse("packs:inventories_provider_list"),
        weight=10,
        icon="bx-right-arrow-alt",
    ),
    MenuItem(
        _("categories").capitalize(),
        reverse("packs:inventories_productcategory_list"),
        weight=11,
        icon="bx-right-arrow-alt",
    ),
    MenuItem(
        _("measures").capitalize(),
        reverse("packs:inventories_measure_list"),
        weight=12,
        icon="bx-right-arrow-alt",
    ),
    MenuItem(
        _("products").capitalize(),
        reverse("packs:inventories_product_list"),
        weight=13,
        icon="bx-right-arrow-alt",
    ),
]

inventories_item = MenuItem(
    _("inventories").capitalize(), "#", icon="bxs-store", children=submenu_items
)
