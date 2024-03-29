from typing import List

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from apps.core.domain.repositories import MenuRepository
from faclab import cache

SRI_CONFIG_CACHE_KEY = "sri_config"


class SRIConfig:
    id = None
    iva_percent = None
    signature = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def iva_rate(self):
        return self.iva_percent / 100 if self.iva_percent else None

    @property
    def iva_factor(self):
        return (self.iva_percent / 100) + 1 if self.iva_percent else None


class SiteService:
    # @cache.set_cache(SRI_CONFIG_CACHE_KEY, [])
    def get_config_object(self):
        from apps.core.models import Site

        return Site.objects.first()

    def get_sri_config(self) -> SRIConfig:
        config = self.get_config_object()
        data_config = {"id": config.id, **config.sri_config} if config else {}
        sri_config = SRIConfig(**data_config)

        return sri_config

    def delete_sri_cache_config(self) -> None:
        cache.delete(SRI_CONFIG_CACHE_KEY)


class MenuService(MenuRepository):
    def retrieve_menu_item(self) -> MenuItem:
        submenu_items = self.retrieve_menu_items()

        return MenuItem(
            _("configuration").capitalize(),
            "#",
            icon="bxs-cog",
            children=submenu_items,
        )

    def retrieve_menu_items(self) -> List[MenuItem]:
        return [
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
                reverse("packs:core_site_update", args=[1]),
                weight=32,
                icon="bx-right-arrow-alt",
            ),
        ]
