from typing import List

from dependency_injector.wiring import Provide, inject
from django.apps import apps
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from apps.core.domain.entities import SRIConfig
from apps.core.domain.repositories import MenuRepository, SiteRepository

SRI_CONFIG_CACHE_KEY = "sri_config"


class SiteRepositoryImpl(SiteRepository):
    def __init__(self) -> None:
        self.model = apps.get_model("core", "Site")
        self.site = self.model.objects.first()

        if not self.site:
            raise self.model.DoesNotExist()

    def get_sri_config(self) -> SRIConfig:
        return SRIConfig(**self.site.sri_config)

    def refresh_site(self) -> None:
        self.site.refresh_from_db()


class MenuRepositoryImpl(MenuRepository):
    @inject
    def __init__(
        self,
        site_repository: SiteRepository = Provide["core_package.site_repository"],
    ) -> None:
        self.site_repository = site_repository

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
                reverse("packs:core_site_update", args=[self.site_repository.site.id]),
                weight=32,
                icon="bx-right-arrow-alt",
            ),
        ]
