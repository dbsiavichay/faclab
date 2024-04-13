from dependency_injector import containers, providers
from zeep import Client

from apps.sri.application.services import SRIVoucherService
from apps.sri.application.usecases import (
    GenerateVoucherAccessCodeUseCase,
    GenerateVoucherXmlUseCase,
    RetrieveVoucherUseCase,
)

from .adapters import SRIVoucherAdapter


class SRIContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # WSDL Clients
    sending_voucher_client = providers.Singleton(Client, wsdl=config.SENDING_VOUCHER_WS)
    query_voucher_client = providers.Singleton(Client, wsdl=config.QUERY_VOUCHER_WS)

    # Adapters
    sri_voucher_adapter = providers.Singleton(
        SRIVoucherAdapter,
        sending_client=sending_voucher_client,
        query_client=query_voucher_client,
    )

    # Usecases
    generate_voucher_access_code_usecase = providers.Singleton(
        GenerateVoucherAccessCodeUseCase
    )
    generate_voucher_xml_usecase = providers.Singleton(GenerateVoucherXmlUseCase)
    retrieve_voucher_usecase = providers.Singleton(
        RetrieveVoucherUseCase, sri_voucher_port=sri_voucher_adapter
    )

    # Services
    sri_voucher_service = providers.Singleton(
        SRIVoucherService,
        generate_access_code_usecase=generate_voucher_access_code_usecase,
        generate_voucher_xml_usecase=generate_voucher_xml_usecase,
        retrieve_voucher_usecase=retrieve_voucher_usecase,
    )
