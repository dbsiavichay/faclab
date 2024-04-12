from dependency_injector import containers, providers

from apps.sale.application.services import InvoiceService
from apps.sale.application.usecases import (
    CalculateInvoiceTotalUseCase,
    GenerateVoucherSequenceUseCase,
)
from apps.sale.infra.repositories import (
    InvoiceLineRepositoryImpl,
    InvoiceRepositoryImpl,
    MenuRepositoryImpl,
    VoucherTypeRepositoryImpl,
)


class SaleContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Container dependencies
    sri_voucher_service = providers.Dependency()

    # Repositories
    invoice_repository = providers.Singleton(InvoiceRepositoryImpl)
    invoiceline_repository = providers.Singleton(InvoiceLineRepositoryImpl)
    menu_repository = providers.Singleton(MenuRepositoryImpl)
    voucher_type_repository = providers.Singleton(VoucherTypeRepositoryImpl)

    # Usecases
    generate_voucher_sequence_usecase = providers.Singleton(
        GenerateVoucherSequenceUseCase, voucher_type_repository=voucher_type_repository
    )
    calculate_invoice_total_usecase = providers.Singleton(
        CalculateInvoiceTotalUseCase, invoiceline_repository=invoiceline_repository
    )

    # Services
    invoice_service = providers.Singleton(
        InvoiceService,
        invoice_repository=invoice_repository,
        invoiceline_repository=invoiceline_repository,
        generate_voucher_sequence_usecase=generate_voucher_sequence_usecase,
        calculate_invoice_total_usecase=calculate_invoice_total_usecase,
        sri_voucher_service=sri_voucher_service,
    )
