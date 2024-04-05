from dependency_injector import containers, providers

from apps.core.application.containers import CoreContainer
from apps.sale.application.containers import SaleContainer


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    core_package = providers.Container(CoreContainer)
    sale_package = providers.Container(SaleContainer)
