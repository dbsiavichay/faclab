import pytest

from apps.inventories.models import Product
from apps.sales.models import Customer, CustomerCodeType


@pytest.fixture
def customer_code_types(db):
    types = [
        ("04", "RUC", 13),
        ("05", "CÉDULA", 10),
        ("06", "PASAPORTE", 99),
        ("07", "VENTA A CONSUMIDOR FINAL", 13),
        ("08", "IDENTIFICACIÓN DEL EXTERIOR", 99),
    ]
    code_types = [
        CustomerCodeType(code=code, name=name, length=long)
        for code, name, long in types
    ]
    CustomerCodeType.objects.bulk_create(code_types)

    return CustomerCodeType.objects.all()


@pytest.fixture
def customer(db, customer_code_types):
    code_type = customer_code_types.filter(code="07").first()
    data = {
        "code_type": code_type,
        "code": "test",
        "bussiness_name": "Test",
        "email": "test@test.com",
    }
    customer = Customer.objects.create(**data)

    return customer


@pytest.fixture
def product(db):
    data = {
        "code": "test",
        "name": "Test",
        "short_name": "Short name test",
        "description": "Product description",
        "is_inventoried": True,
        "apply_iva": True,
        "apply_ice": False,
    }
    return Product.objects.create(**data)
