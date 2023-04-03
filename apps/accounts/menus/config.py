from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

submenu_items = [
    MenuItem(
        _("sri").upper(),
        reverse("packs:sites_config_list"),
        weight=30,
        icon="bx-right-arrow-alt",
    ),
]

config_item = MenuItem(
    _("configuration").capitalize(), "#", icon="bxs-cog", children=submenu_items
)
