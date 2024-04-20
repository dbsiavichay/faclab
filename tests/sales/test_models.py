import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from django.forms.models import model_to_dict

from apps.sale.application.validators import customer_code_validator
from apps.sale.infra.models import Customer, CustomerCodeType, Invoice, InvoiceLine


class TestCustomerCodeType:
    def test_settings(self):
        assert "apps.sale" in settings.INSTALLED_APPS

    @pytest.mark.django_db
    def test_customer_code_type_create(self):
        data = {"code": "04", "name": "Test", "length": 10}
        code_type = CustomerCodeType.objects.create(**data)

        assert isinstance(code_type, CustomerCodeType)
        assert data == model_to_dict(code_type, fields=data.keys())


class TestCustomer:
    @pytest.mark.django_db
    def test_customer_create(self, customer_code_types):
        code_type = customer_code_types.first()

        data = {
            "code_type": code_type,
            "code": "test",
            "bussiness_name": "Test",
            "email": "test@test.com",
        }
        customer = Customer.objects.create(**data)
        data.update({"code_type": code_type.id})

        assert isinstance(customer, Customer)
        assert customer.first_name is None
        assert customer.last_name is None
        assert customer.address is None
        assert customer.phone is None

        assert data == model_to_dict(customer, fields=data.keys())

    @pytest.mark.parametrize(
        "code",
        [
            "0941531600",
            "1105071342",
            "0900041732",
            "1400690143001",
            "0941531600001",
            "1105071342001",
            "0900041732001",
        ],
    )
    def test_customer_code_validator(self, code):
        customer_code_validator(code)
        assert True

    @pytest.mark.parametrize(
        "code",
        [12345, "12345", "1234a", "1234567890", "9999999999"],
    )
    def test_customer_code_validator_fail(self, code):
        with pytest.raises(ValidationError):
            customer_code_validator(code)


class TestInvoice:
    @pytest.mark.django_db
    def test_invoice_create(self, customer, product, sri_config):
        data = {
            "company_branch_code": "tst",
            "company_sale_point_code": "tst",
            "sequence": "tst",
            "customer": customer,
        }
        invoice = Invoice.objects.create(**data)
        data.update({"customer": customer.id})

        assert isinstance(invoice, Invoice)
        assert invoice.number == "tst-tst-tst"
        assert data == model_to_dict(invoice, fields=data.keys())

        line_data = {
            "quantity": 1,
            "unit_price": 100,
            "product": product,
            "invoice": invoice,
            "subtotal": 100,
            "tax": 12,
            "total": 112,
        }

        line = InvoiceLine.objects.create(**line_data)
        line.save()
        line_data.update({"product": product.id, "invoice": invoice.id})

        assert isinstance(line, InvoiceLine)
        assert line_data == model_to_dict(line, fields=line_data.keys())

    @pytest.mark.django_db
    def test_invoice_create_fail(self, customer):
        data = {
            "company_branch_code": "test",
            "company_sale_point_code": "test",
            "sequence": "test",
            "customer": customer,
        }
        with pytest.raises(DataError):
            Invoice.objects.create(**data)
