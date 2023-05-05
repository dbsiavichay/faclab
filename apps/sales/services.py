from tempfile import NamedTemporaryFile

import xmltodict
from django.core.files import File
from django.core.files.base import ContentFile
from django.db.models import Sum

from apps.sites.services import SRIConfigService

from .models import VoucherType


class InvoiceService:
    INVOICE_CODE = "01"

    @classmethod
    def get_sequence(cls):
        sequence = 1
        voucher_type = VoucherType.objects.filter(code=cls.INVOICE_CODE).first()

        if voucher_type:
            voucher_type.current = voucher_type.current + 1
            voucher_type.save(update_fields=["current"])

            return voucher_type.current

        return sequence

    @classmethod
    def generate_access_code(cls, invoice):
        config = SRIConfigService.get_sri_config()
        date = invoice.date.strftime("%d%m%Y")
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
        invoice.save(update_fields=["code"])

    @classmethod
    def calculate_totals(cls, invoice):
        config = SRIConfigService.get_sri_config()
        subtotal = invoice.lines.aggregate(subtotal=Sum("subtotal")).get("subtotal")
        invoice.subtotal = subtotal
        invoice.tax = subtotal * config.iva_rate
        invoice.total = subtotal * config.iva_factor
        invoice.save(update_fields=["subtotal", "tax", "total"])

    @classmethod
    def calculate_line_totals(cls, invoice_line):
        config = SRIConfigService.get_sri_config()
        invoice_line.subtotal = invoice_line.unit_price * invoice_line.quantity
        invoice_line.tax = invoice_line.subtotal * config.iva_rate
        invoice_line.total = invoice_line.subtotal * config.iva_factor

        return invoice_line

    @classmethod
    def get_xml_data(cls, invoice):
        config = SRIConfigService.get_sri_config()

        data = {
            "factura": {
                "@id": "comprobante",
                "@version": "1.1.0",
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
                    "fechaEmision": invoice.date.strftime("%d/%m/%Y"),
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
                    "importeTotal": invoice.total,
                    "moneda": "DOLAR",
                    "pagos": {
                        "pago": [
                            {
                                "formaPago": "01",
                                "total": invoice.total,
                                "plazo": 0,
                                "unidadTiempo": "dias",
                            }
                        ]
                    },
                },
                "detalles": {"detalle": []},
                "infoAdicional": {
                    "campoAdicional": [
                        {"@nombre": "Dirección", "#text": invoice.customer.address},
                        {"@nombre": "Telefono", "#text": invoice.customer.phone},
                        {"@nombre": "Email", "#text": invoice.customer.email},
                    ]
                },
            }
        }

        for line in invoice.lines.select_related("product").all():
            data["factura"]["detalles"]["detalle"].append(
                {
                    "codigoPrincipal": line.product.code,
                    "codigoAuxiliar": line.product.code,
                    "descripcion": line.product.name,
                    "cantidad": line.quantity,
                    "precioUnitario": line.unit_price,
                    "descuento": 0,
                    "precioTotalSinImpuestos": line.subtotal,
                    "impuestos": {
                        "impuesto": [
                            {
                                "codigo": 2,
                                "codigoPorcentaje": 2,
                                "tarifa": config.iva_percent,
                                "baseImponible": line.subtotal,
                                "valor": line.tax,
                            }
                        ]
                    },
                }
            )

        return data

    @classmethod
    def generate_xml(cls, invoice):
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
        invoice.save(update_fields=["file"])

        return file
