import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

from apps.customers.enums import CodeTypes
from apps.customers.models import Customer
from apps.customers.validators import code_validator


class TestCustomer:
    def test_settings(self):
        assert "apps.customers" in settings.INSTALLED_APPS

    @pytest.mark.django_db
    def test_customer_create(self):
        data = {
            "code_type": CodeTypes.CHARTER,
            "code": "test",
            "bussiness_name": "Test",
            "email": "test@test.com",
        }
        customer = Customer.objects.create(**data)

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
    def test_validate_code(self, code):
        code_validator(code)
        assert True

    @pytest.mark.parametrize(
        "code",
        [12345, "12345", "1234a", "1234567890", "9999999999"],
    )
    def test_validate_code_fail(self, code):
        with pytest.raises(ValidationError):
            code_validator(code)
