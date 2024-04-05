from dependency_injector import containers, providers

from apps.sale.application.services import InvoiceService
from apps.sale.application.usecases import GenerateVoucherSequenceUseCase
from apps.sale.infra.adapters import InvoiceAdapter, VoucherTypeAdapter


class SaleContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Repositories
    voucher_type_adapter = providers.Singleton(VoucherTypeAdapter)
    invoice_adapter = providers.Singleton(InvoiceAdapter)

    # Usecases
    generate_voucher_sequence_usecase = providers.Singleton(
        GenerateVoucherSequenceUseCase, voucher_type_repository=voucher_type_adapter
    )

    # Services
    invoice_service = providers.Singleton(
        InvoiceService,
        generate_voucher_sequence_port=generate_voucher_sequence_usecase,
        invoice_repository=invoice_adapter,
    )
