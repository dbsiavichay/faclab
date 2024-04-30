from dependency_injector.wiring import Provide, inject
from django import forms

from apps.sale.application.services import InvoiceService
from apps.sale.domain.entities import InvoiceEntity

from .forms import InvoiceLineForm
from .models import Invoice, InvoiceLine, InvoicePayment


class InvoiceLineInlineFormset(forms.BaseInlineFormSet):
    @inject
    def __init__(
        self,
        invoice_service: InvoiceService = Provide["sale_package.invoice_service"],
        *args,
        **kwargs
    ) -> None:
        self.invoice_service = invoice_service
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        object_list = super().save(commit=commit)
        invoice_entity = InvoiceEntity(**self.instance.__dict__)
        self.invoice_service.update_invoice_access_code(invoice_entity)
        self.invoice_service.update_invoice_total(invoice_entity)
        update_fields = ["access_code", "subtotal", "tax", "total"]
        self.instance.__dict__.update(invoice_entity.model_dump(include=update_fields))
        self.instance.save(update_fields=update_fields)

        return object_list


InvoiceLineFormset = forms.inlineformset_factory(
    Invoice,
    InvoiceLine,
    form=InvoiceLineForm,
    formset=InvoiceLineInlineFormset,
    extra=1,
    min_num=1,
    validate_min=True,
)

InvoicePaymentFormset = forms.inlineformset_factory(
    Invoice,
    InvoicePayment,
    fields=("type", "amount"),
    extra=1,
)
