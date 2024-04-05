from django.db.models import Sum

from apps.core.infra.adapters import SiteAdapter

site_adapter = SiteAdapter()


class PurchaseService:
    @classmethod
    def calculate_totals(cls, purchase, commit=True):
        config = site_adapter.get_sri_config()
        subtotal = purchase.lines.aggregate(subtotal=Sum("subtotal")).get("subtotal")
        purchase.subtotal = subtotal
        purchase.tax = subtotal * config.iva_rate
        purchase.total = subtotal * config.iva_factor

        if commit:
            purchase.save(update_fields=["subtotal", "tax", "total"])

    @classmethod
    def calculate_line_totals(cls, purchase_line):
        config = site_adapter.get_sri_config()
        purchase_line.subtotal = purchase_line.unit_price * purchase_line.quantity
        purchase_line.tax = purchase_line.subtotal * config.iva_rate
        purchase_line.total = purchase_line.subtotal * config.iva_factor

        return purchase_line
