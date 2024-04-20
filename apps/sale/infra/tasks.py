from faclab.celery import app
from faclab.containers import build_container


@app.task
def send_invoice_task(
    invoice_id: int,
):
    container = build_container()
    invoice_service = container.sale_package().invoice_service()
    invoice_entity = invoice_service.invoice_repository.find_by_id(invoice_id)
    invoice_service.send_invoice_xml(invoice_entity, update_on_db=True)
