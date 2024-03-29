from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from apps.core.application.services import SiteService

service = SiteService()
sri_config = service.get_sri_config()

submenu_items = [
    MenuItem(
        _("vouchers").capitalize(),
        reverse("packs:sales_vouchertype_list"),
        weight=30,
        icon="bx-right-arrow-alt",
    ),
    MenuItem(
        _("signatures").capitalize(),
        reverse("packs:core_signature_list"),
        weight=31,
        icon="bx-right-arrow-alt",
    ),
    MenuItem(
        _("sri").upper(),
        reverse("packs:core_site_update", args=[sri_config.id]),
        weight=32,
        icon="bx-right-arrow-alt",
    ),
]

config_item = MenuItem(
    _("configuration").capitalize(), "#", icon="bxs-cog", children=submenu_items
)
