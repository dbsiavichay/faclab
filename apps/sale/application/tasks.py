from celery import chain

from apps.sale.models import Invoice
from faclab.celery import app

from .services import InvoiceService


@app.task
def sign_invoice_task(invoice_id):
    invoice = Invoice.objects.filter(id=invoice_id).first()
    InvoiceService.generate_xml(invoice)
    InvoiceService.sign_xml(invoice)

    return invoice_id


@app.task
def send_invoice_task(invoice_id):
    invoice = Invoice.objects.filter(id=invoice_id).first()
    InvoiceService.send_xml(invoice)

    return invoice_id


sign_and_send_invoice_task = chain(sign_invoice_task.s(), send_invoice_task.s())
