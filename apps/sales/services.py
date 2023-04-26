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
