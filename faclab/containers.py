from dependency_injector import containers, providers

from apps.core.infra.containers import CoreContainer
from apps.sale.infra.containers import SaleContainer
from apps.sri.infra.containers import SRIContainer

from . import settings


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    core_package = providers.Container(CoreContainer)
    sri_package = providers.Container(SRIContainer, config=config.SRI_SERVICES)
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
            "apps.sale.application.services",
            "apps.sale.infra.forms",
            "apps.sale.packs",
            "apps.sri.application.services",
        ]
    )

    return container
