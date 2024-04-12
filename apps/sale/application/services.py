from tempfile import NamedTemporaryFile

import pytz
import xmltodict
from dependency_injector.wiring import Provide, inject
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile

from apps.core.domain.repositories import SiteRepository
from apps.core.infra.repositories import SiteRepositoryImpl
from apps.sale.application.usecases import (
    CalculateInvoiceTotalUseCase,
    GenerateVoucherSequenceUseCase,
)
from apps.sale.domain.entities import InvoiceEntity, InvoiceLineEntity
from apps.sale.domain.enums import VoucherStatuses
from apps.sale.domain.repositories import InvoiceLineRepository, InvoiceRepository
from apps.sri.application.services import SRIClient, SRISigner, SRIVoucherService

site_repository = SiteRepositoryImpl()


class InvoiceService:
    @inject
    def __init__(
        self,
        invoice_repository: InvoiceRepository,
        invoiceline_repository: InvoiceLineRepository,
        generate_voucher_sequence_usecase: GenerateVoucherSequenceUseCase,
        calculate_invoice_total_usecase: CalculateInvoiceTotalUseCase,
        sri_voucher_service: SRIVoucherService,
        site_repository: SiteRepository = Provide["core_package.site_repository"],
    ) -> None:
        self.invoice_voucher_type_code = "01"
        self.invoice_repository = invoice_repository
        self.invoiceline_repository = invoiceline_repository
        self.generate_voucher_sequence_usecase = generate_voucher_sequence_usecase
        self.calculate_invoice_total_usecase = calculate_invoice_total_usecase
        self.sri_voucher_service = sri_voucher_service
        self.site_repository = site_repository

    def update_invoice_sequence(
        self, invoice_entity: InvoiceEntity, update_on_db: bool = False
    ) -> str:
        invoice_entity.sequence = self.generate_voucher_sequence_usecase.execute(
            self.invoice_voucher_type_code
        )

        if update_on_db:
            self.invoice_repository.save(invoice_entity, update_fields=["sequence"])

        return invoice_entity

    def update_invoice_access_code(
        self, invoice_entity: InvoiceEntity, update_on_db: bool = False
    ) -> InvoiceEntity:
        invoice_entity.code = self.sri_voucher_service.generate_access_code(
            self.invoice_voucher_type_code,
            invoice_entity.id,
            invoice_entity.issue_date,
            invoice_entity.sequence,
        )

        if update_on_db:
            self.invoice_repository.save(invoice_entity, update_fields=["code"])

        return invoice_entity

    def update_invoice_line_total(
        self, invoiceline_entity: InvoiceLineEntity, update_on_db: bool = False
    ) -> InvoiceLineEntity:
        sri_config = self.site_repository.get_sri_config()
        invoiceline_entity = (
            self.calculate_invoice_total_usecase.execute_by_invoiceline(
                invoiceline_entity, sri_config
            )
        )

        if update_on_db:
            self.invoiceline_repository.save(
                invoiceline_entity, update_fields=["subtotal", "tax", "total"]
            )

        return invoiceline_entity

    def update_invoice_total(
        self, invoice_entity: InvoiceEntity, update_on_db: bool = False
    ) -> InvoiceEntity:
        sri_config = self.site_repository.get_sri_config()
        invoice_entity = self.calculate_invoice_total_usecase.execute_by_invoice(
            invoice_entity, sri_config
        )

        if update_on_db:
            self.invoice_repository.save(
                invoice_entity, update_fields=["subtotal", "tax", "total"]
            )

        return invoice_entity


class InvoiceServiceLegacy:
    INVOICE_CODE = "01"

    @classmethod
    def get_xml_data(cls, invoice):
        config = site_repository.get_sri_config()
        timezone = pytz.timezone(settings.TIME_ZONE)
        invoice_date = invoice.issue_date.astimezone(timezone)

        data = {
            "factura": {
                "@id": "comprobante",
                "@version": "1.0.0",
                "infoTributaria": {
                    "ambiente": config.environment,
                    "tipoEmision": config.emission,
                    "razonSocial": config.company_name,
                    "nombreComercial": config.trade_name,
                    "ruc": config.code,
                    "claveAcceso": invoice.code,
                    "codDoc": cls.INVOICE_CODE,
                    "estab": invoice.company_code,
                    "ptoEmi": invoice.company_point_sale_code,
                    "secuencial": invoice.sequence,
                    "dirMatriz": config.main_address,
                },
                "infoFactura": {
                    "fechaEmision": invoice_date.strftime("%d/%m/%Y"),
                    "dirEstablecimiento": config.company_address,
                    # "contribuyenteEspecial": "1234",
                    "obligadoContabilidad": "SI"
                    if config.accounting_required
                    else "NO",
                    "tipoIdentificacionComprador": invoice.customer.code_type.code,
                    "razonSocialComprador": invoice.customer.bussiness_name,
                    "identificacionComprador": invoice.customer.code,
                    "totalSinImpuestos": invoice.subtotal,
                    "totalDescuento": 0,
                    "totalConImpuestos": {
                        "totalImpuesto": [
                            {
                                "codigo": 2,
                                "codigoPorcentaje": 4,
                                "baseImponible": invoice.subtotal,
                                "valor": invoice.tax,
                            }
                        ]
                    },
                    "propina": 0,
                    "importeTotal": round(invoice.total, 2),
                    "moneda": "DOLAR",
                    "pagos": {"pago": []},
                },
                "detalles": {"detalle": []},
                "infoAdicional": {"campoAdicional": []},
            }
        }

        customer = invoice.customer

        if customer.address:
            data["factura"]["infoAdicional"]["campoAdicional"].append(
                {"@nombre": "Dirección", "#text": customer.address}
            )

        if customer.phone:
            data["factura"]["infoAdicional"]["campoAdicional"].append(
                {"@nombre": "Telefono", "#text": customer.phone}
            )

        data["factura"]["infoAdicional"]["campoAdicional"].append(
            {"@nombre": "Email", "#text": customer.email}
        )

        for payment in invoice.payments.all():
            data["factura"]["infoFactura"]["pagos"]["pago"].append(
                {
                    "formaPago": payment.type,
                    "total": round(payment.amount, 2),
                    "plazo": 0,
                    "unidadTiempo": "dias",
                }
            )

        for line in invoice.lines.select_related("product").all():
            data["factura"]["detalles"]["detalle"].append(
                {
                    "codigoPrincipal": line.product.code,
                    "codigoAuxiliar": line.product.code,
                    "descripcion": line.product.name,
                    "cantidad": line.quantity,
                    "precioUnitario": line.unit_price,
                    "descuento": 0,
                    "precioTotalSinImpuesto": line.subtotal,
                    "impuestos": {
                        "impuesto": [
                            {
                                "codigo": 2,
                                "codigoPorcentaje": 4,
                                "tarifa": int(config.iva_percent),
                                "baseImponible": line.subtotal,
                                "valor": line.tax,
                            }
                        ]
                    },
                }
            )

        return data

    @classmethod
    def generate_xml(cls, invoice, commit=True):
        data = cls.get_xml_data(invoice)
        xml = xmltodict.unparse(data, pretty=True)
        xml_file = NamedTemporaryFile(suffix=".xml")

        with open(xml_file.name, "w") as file:
            file.write(xml)

        file.close()

        file_name = f"{invoice.code}.xml"
        content_file = ContentFile(xml_file.read())
        file = File(file=content_file, name=file_name)
        invoice.file = file

        if commit:
            invoice.save(update_fields=["file"])

        return file

    @classmethod
    def sign_xml(cls, invoice):
        signer = SRISigner()
        str_signed_invoice = signer.sign(invoice.file.read())
        xml_file = NamedTemporaryFile(suffix=".xml")

        with open(xml_file.name, "w") as file:
            file.write(str_signed_invoice)

        file.close()
        file_name = f"{invoice.code}.xml"
        content_file = ContentFile(xml_file.read())
        file = File(file=content_file, name=file_name)
        invoice.file.delete()
        invoice.file = file
        invoice.status = VoucherStatuses.SIGNED
        invoice.save(update_fields=["status", "file"])

        return file

    @classmethod
    def send_xml(cls, invoice):
        client = SRIClient()
        client.send_voucher(invoice.file.read())
        _, authotization_date = client.fetch_voucher(invoice.code)
        invoice.authorization_date = authotization_date
        invoice.status = VoucherStatuses.AUTHORIZED
        invoice.save(update_fields=["authorization_date", "status"])
