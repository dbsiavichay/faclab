from dependency_injector import containers, providers

from apps.sale.application.services import InvoiceService
from apps.sale.application.usecases import GenerateVoucherSequenceUseCase
from apps.sale.infra.repositories import (
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
    menu_repository = providers.Singleton(MenuRepositoryImpl)
    voucher_type_repository = providers.Singleton(VoucherTypeRepositoryImpl)

    # Usecases
    generate_voucher_sequence_usecase = providers.Singleton(
        GenerateVoucherSequenceUseCase, voucher_type_repository=voucher_type_repository
    )

    # Services
    invoice_service = providers.Singleton(
        InvoiceService,
        invoice_repository=invoice_repository,
        generate_voucher_sequence_usecase=generate_voucher_sequence_usecase,
        sri_voucher_service=sri_voucher_service,
    )
