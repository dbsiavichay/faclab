from tempfile import NamedTemporaryFile

import pytz
import xmltodict
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.db.models import Sum

from apps.core.infra.adapters import SiteAdapter
from apps.sale.domain.enums import VoucherStatuses
from apps.sale.domain.models import VoucherType
from apps.sri.services import SRIClient, SRISigner

site_adapter = SiteAdapter()


class InvoiceService:
    INVOICE_CODE = "01"

    @classmethod
    def generate_sequence(cls, invoice, commit=True):
        sequence = 1
        voucher_type = VoucherType.objects.filter(code=cls.INVOICE_CODE).first()

        if voucher_type:
            voucher_type.current = voucher_type.current + 1
            voucher_type.save(update_fields=["current"])
            sequence = voucher_type.current

        invoice.sequence = str(sequence).zfill(9)

        if commit:
            invoice.save(update_fields=["sequence"])

        return sequence

    @classmethod
    def generate_access_code(cls, invoice, commit=True):
        config = site_adapter.get_sri_config()
        timezone = pytz.timezone(settings.TIME_ZONE)
        invoice_date = invoice.issue_date.astimezone(timezone)
        date = invoice_date.strftime("%d%m%Y")
        doc = cls.INVOICE_CODE
        env = config.environment
        serie = f"{config.company_code}{config.company_point_sale_code}"
        seq = invoice.sequence
        number = str(invoice.id)[:8].zfill(8)
        emission = config.emission
        code = f"{date}{doc}{config.code}{env}{serie}{seq}{number}{emission}"

        factor = 2
        sum = 0

        reversed_code = code[::-1]

        for char in reversed_code:
            number = int(char)
            number = number * factor
            sum = sum + number
            factor = factor + 1
            factor = 2 if factor > 7 else factor

        verifier = 11 - (sum % 11)
        verifier = 0 if verifier == 11 else 1 if verifier == 10 else verifier
        code = f"{code}{verifier}"
        invoice.code = code

        if commit:
            invoice.save(update_fields=["code"])

    @classmethod
    def calculate_totals(cls, invoice, commit=True):
        config = site_adapter.get_sri_config()
        subtotal = invoice.lines.aggregate(subtotal=Sum("subtotal")).get("subtotal")
        invoice.subtotal = subtotal
        invoice.tax = subtotal * config.iva_rate
        invoice.total = subtotal * config.iva_factor

        if commit:
            invoice.save(update_fields=["subtotal", "tax", "total"])

    @classmethod
    def calculate_line_totals(cls, invoice_line):
        config = site_adapter.get_sri_config()
        invoice_line.subtotal = invoice_line.unit_price * invoice_line.quantity
        invoice_line.tax = invoice_line.subtotal * config.iva_rate
        invoice_line.total = invoice_line.subtotal * config.iva_factor

        return invoice_line

    @classmethod
    def get_xml_data(cls, invoice):
        config = site_adapter.get_sri_config()
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
                                "codigoPorcentaje": 2,
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
                                "codigoPorcentaje": 2,
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
