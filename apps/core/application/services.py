from typing import List

from dependency_injector.wiring import Provide, inject
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from apps.core.domain.entities import SRIConfig
from apps.core.domain.repositories import MenuRepository, SiteRepository

# from faclab import cache

SRI_CONFIG_CACHE_KEY = "sri_config"


class SiteService(SiteRepository):
    # @cache.set_cache(SRI_CONFIG_CACHE_KEY, [])
    def get_current_site(self):
        from apps.core.models import Site

        return Site.objects.first()

    def get_site_id(self) -> int:
        site = self.get_current_site()
        return site.id

    def get_sri_config(self) -> SRIConfig:
        site = self.get_current_site()
        sri_config = SRIConfig(**site.sri_config)

        return sri_config

    def delete_sri_cache_config(self) -> None:
        pass
        # cache.delete(SRI_CONFIG_CACHE_KEY)


class MenuService(MenuRepository):
    @inject
    def __init__(
        self,
        site_service: SiteRepository = Provide["core_package.site_service"],
    ) -> None:
        self.site_service = site_service

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
                reverse("packs:sale_vouchertype_list"),
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
                reverse(
                    "packs:core_site_update", args=[self.site_service.get_site_id()]
                ),
                weight=32,
                icon="bx-right-arrow-alt",
            ),
        ]
