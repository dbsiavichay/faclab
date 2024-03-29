from dependency_injector import containers, providers

from apps.core.application.containers import CoreContainer


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    core_package = providers.Container(CoreContainer)
