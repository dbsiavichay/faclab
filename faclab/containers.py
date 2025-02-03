from dependency_injector import containers, providers

from apps.core.infra.containers import CoreContainer
from apps.inventory.infra.containers import InventoryContainer
from apps.purchase.infra.containers import PurchaseContainer
from apps.sale.infra.containers import SaleContainer
from apps.sri.infra.containers import SRIContainer

from . import settings


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    core_package = providers.Container(CoreContainer, config=config)
    inventory_package = providers.Container(InventoryContainer)
    purchase_package = providers.Container(PurchaseContainer)
    sri_package = providers.Container(SRIContainer, config=config.SRI_PACKAGE)
    sale_package = providers.Container(
        SaleContainer, sri_voucher_service=sri_package.sri_voucher_service
    )


def build_container():
    container = ApplicationContainer()
    container.config.from_dict(settings.__dict__)

    container.wire(
        modules=[
            "apps.core.application.main_menu",
            "apps.core.infra.forms",
            "apps.core.infra.repositories",
            "apps.core.infra.views",
            "apps.purchase.application.services",
            "apps.purchase.infra.forms",
            "apps.purchase.infra.formsets",
            "apps.sale.application.services",
            "apps.sale.infra.forms",
            "apps.sale.infra.formsets",
            "apps.sale.packs",
            "apps.sri.application.services",
        ]
    )

    return container
