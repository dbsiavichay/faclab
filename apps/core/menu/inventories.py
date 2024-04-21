from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

submenu_items = [
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

inventory_item = MenuItem(
    _("inventory").capitalize(), "#", icon="bxs-store", children=submenu_items
)
