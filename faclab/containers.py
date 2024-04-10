from dependency_injector import containers, providers

from apps.core.application.containers import CoreContainer
from apps.sale.application.containers import SaleContainer
from apps.sri.infra.containers import SRIContainer


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    core_package = providers.Container(CoreContainer)
    sri_package = providers.Container(SRIContainer, config=config.SRI_SERVICES)
    sale_package = providers.Container(
        SaleContainer, sri_voucher_service=sri_package.sri_voucher_service
    )
