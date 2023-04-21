from django.db.models import Sum


class InvoiceService:
    @classmethod
    def calculate_totals(cls, invoice):
        subtotal = invoice.lines.aggregate(subtotal=Sum("subtotal")).get("subtotal")
        invoice.subtotal = subtotal
        invoice.tax = subtotal * 0.12
        invoice.total = subtotal * 1.12
        invoice.save(update_fields=["subtotal", "tax", "total"])
