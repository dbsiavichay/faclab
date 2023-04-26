import pytest
from django.forms.models import model_to_dict

from apps.sales.forms import CustomerForm, InvoiceForm, InvoiceLineFormset
from apps.sales.models import Customer, Invoice, InvoiceLine


class TestCustomerForm:
    @pytest.mark.django_db
    def test_customer_create(self, customer_code_types):
        code_type = customer_code_types.first()
        data = {
            "code_type": code_type.id,
            "code": "0941531600001",
            "bussiness_name": "test",
            "email": "test@test.com",
        }
        form = CustomerForm(data)
        customer = form.save()

        assert form.is_valid() is True
        assert not form.errors
        assert isinstance(customer, Customer)
        assert data == model_to_dict(customer, fields=data.keys())

    @pytest.mark.parametrize(
        "code_type, code",
        [("04", "0941531600"), ("05", "0941531600001"), ("05", "0941531500001")],
    )
    @pytest.mark.django_db
    def test_customer_create_invalid(self, code_type, code, customer_code_types):
        code_type = customer_code_types.get(code=code_type)
        data = {
            "code_type": code_type.id,
            "code": code,
            "bussiness_name": "test",
            "email": "test@test.com",
        }
        form = CustomerForm(data)
        assert form.is_valid() is False
        assert form.errors


class TestInvoiceForm:
    @pytest.mark.django_db
    def test_invoice_create(self, customer, product, sri_config):
        data = {"customer": customer}

        form = InvoiceForm(data)
        invoice = form.save()

        line_data = {
            "lines-0-quantity": 1,
            "lines-0-unit_price": 100,
            "lines-0-product": product,
            "lines-TOTAL_FORMS": 1,
            "lines-INITIAL_FORMS": 0,
            "lines-MIN_NUM_FORMS": 1,
            "lines-MAX_NUM_FORMS": 1000,
        }

        formset = InvoiceLineFormset(line_data, instance=invoice)
        formset.is_valid()
        lines = formset.save()
        line = lines[0]

        assert form.is_valid() is True
        assert not form.errors
        assert isinstance(invoice, Invoice)
        assert invoice.customer == customer
        assert invoice.number == "001-001-000000001"
        assert round(invoice.subtotal, 5) == 100
        assert round(invoice.tax, 5) == 12
        assert round(invoice.total, 5) == 112

        assert formset.is_valid() is True

        assert isinstance(line, InvoiceLine)
        assert line.invoice == invoice
        assert round(invoice.subtotal, 5) == 100
        assert round(invoice.tax, 5) == 12
        assert round(invoice.total, 5) == 112

    @pytest.mark.django_db
    def test_invoice_create_invalid(self):
        data = {}

        form = InvoiceForm(data)
        form = InvoiceForm(data)
        assert form.is_valid() is False
