import pytest

from apps.sales.models import CustomerCodeType


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
