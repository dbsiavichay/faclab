from dependency_injector import containers, providers
from zeep import Client

from apps.sri.application.services import SRIVoucherService
from apps.sri.application.usecases import (
    GenerateVoucherAccessCodeUseCase,
    GenerateVoucherXmlUseCase,
    RetrieveVoucherXmlUseCase,
    SendVoucherXmlUseCase,
    SignVoucherXmlUseCase,
)

from .adapters import SRIVoucherAdapter


class SRIContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # WSDL Clients
    sri_voucher_client = providers.Singleton(Client, wsdl=config.SENDING_VOUCHER_WS)
    sri_authorization_client = providers.Singleton(Client, wsdl=config.QUERY_VOUCHER_WS)

    # Adapters
    sri_voucher_adapter = providers.Singleton(
        SRIVoucherAdapter,
        voucher_client=sri_voucher_client,
        authorization_client=sri_authorization_client,
    )

    # Usecases
    generate_voucher_access_code_usecase = providers.Singleton(
        GenerateVoucherAccessCodeUseCase
    )
    generate_voucher_xml_usecase = providers.Singleton(GenerateVoucherXmlUseCase)
    sign_voucher_xml_usecase = providers.Singleton(SignVoucherXmlUseCase)
    send_voucher_xml_usecase = providers.Singleton(
        SendVoucherXmlUseCase, sri_voucher_port=sri_voucher_adapter
    )
    retrieve_voucher_xml_usecase = providers.Singleton(
        RetrieveVoucherXmlUseCase, sri_voucher_port=sri_voucher_adapter
    )

    # Services
    sri_voucher_service = providers.Singleton(
        SRIVoucherService,
        generate_access_code_usecase=generate_voucher_access_code_usecase,
        generate_voucher_xml_usecase=generate_voucher_xml_usecase,
        sign_voucher_xml_usecase=sign_voucher_xml_usecase,
        send_voucher_xml_usecase=send_voucher_xml_usecase,
        retrieve_voucher_xml_usecase=retrieve_voucher_xml_usecase,
    )
