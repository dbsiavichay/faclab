from celery import chain

from apps.sale.models import Invoice
from faclab.celery import app

from .services import InvoiceServiceLegacy


@app.task
def sign_invoice_task(invoice_id):
    invoice = Invoice.objects.filter(id=invoice_id).first()
    InvoiceServiceLegacy.generate_xml(invoice)
    InvoiceServiceLegacy.sign_xml(invoice)

    return invoice_id


@app.task
def send_invoice_task(invoice_id):
    invoice = Invoice.objects.filter(id=invoice_id).first()
    InvoiceServiceLegacy.send_xml(invoice)

    return invoice_id


sign_and_send_invoice_task = chain(sign_invoice_task.s(), send_invoice_task.s())
