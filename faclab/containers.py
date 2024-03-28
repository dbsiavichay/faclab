from dependency_injector import containers, providers

from apps.sites.application.containers import SitesContainer


class ApplicationContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    sites_package = providers.Container(SitesContainer)
