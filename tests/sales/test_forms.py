import pytest
from django.forms.models import model_to_dict

from apps.sales.forms import CustomerForm
from apps.sales.models import Customer


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
