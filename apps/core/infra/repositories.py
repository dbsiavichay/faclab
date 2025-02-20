from typing import List

from dependency_injector.wiring import Provide, inject
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from pydantic import ValidationError
from simple_menu import MenuItem

from apps.core.application.exceptions import ImproperlyConfigException
from apps.core.domain.entities import SRIConfig
from apps.core.domain.repositories import MenuRepository, SiteRepository

from .models import Site

SRI_CONFIG_CACHE_KEY = "sri_config"


class SiteRepositoryImpl(SiteRepository):
    def __init__(self) -> None:
        self.site = Site.objects.first()

        if not self.site:
            raise ImproperlyConfigException(_("site config does not exist"))

    def get_sri_config(self) -> SRIConfig:
        try:
            return SRIConfig(**self.site.sri_config)
        except ValidationError:
            raise ImproperlyConfigException(
                _("sri config does not exist or is incorrect")
            )

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
                reverse("certificate_list"),
                weight=31,
                icon="bx-right-arrow-alt",
            ),
            MenuItem(
                _("taxes").capitalize(),
                reverse("packs:core_tax_list"),
                weight=32,
                icon="bx-right-arrow-alt",
            ),
            MenuItem(
                _("sri").upper(),
                reverse("packs:core_site_update", args=[self.site_repository.site.id]),
                weight=33,
                icon="bx-right-arrow-alt",
            ),
        ]
