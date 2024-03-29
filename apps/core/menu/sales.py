from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

submenu_items = [
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

sales_item = MenuItem(
    _("sales").capitalize(), "#", icon="bxs-shopping-bag", children=submenu_items
)
