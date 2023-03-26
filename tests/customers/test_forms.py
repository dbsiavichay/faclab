import pytest
from django.forms.models import model_to_dict

from apps.customers.enums import CodeTypes
from apps.customers.forms import CustomerForm
from apps.customers.models import Customer


class TestCustomerForm:
    @pytest.mark.django_db
    def test_customer_create(self):
        data = {
            "code_type": CodeTypes.CHARTER,
            "code": "0941531600",
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
        [(CodeTypes.CHARTER, "0941531600001"), (CodeTypes.RUC, "0941531600")],
    )
    @pytest.mark.django_db
    def test_customer_create_invalid(self, code_type, code):
        data = {
            "code_type": code_type,
            "code": code,
            "bussiness_name": "test",
            "email": "test@test.com",
        }
        form = CustomerForm(data)
        assert form.is_valid() is False
        assert form.errors
