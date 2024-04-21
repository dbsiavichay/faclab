import pytest
from django.forms.models import model_to_dict

from apps.inventory.forms import ProductForm, ProviderForm
from apps.inventory.models import Product, Provider

IVA_RATE = 1.12


class TestProviderForm:
    @pytest.mark.django_db
    def test_provider_create(self):
        data = {
            "code": "0941531600001",
            "bussiness_name": "test",
            "contact_name": "test",
            "address": "test",
            "phone": "0912345678",
            "email": "test@test.com",
        }
        form = ProviderForm(data)
        provider = form.save()

        assert form.is_valid() is True
        assert not form.errors
        assert isinstance(provider, Provider)
        assert data == model_to_dict(provider, fields=data.keys())

    @pytest.mark.parametrize(
        "code",
        ["0941531600", "0941531600001", "0941531500001"],
    )
    @pytest.mark.django_db
    def test_customer_create_invalid(self, code):
        data = {
            "code": code,
            "bussiness_name": "test",
            "contact_name": "test",
            "phone": "0912345678",
            "email": "test@test.com",
        }
        form = ProviderForm(data)
        assert form.is_valid() is False
        assert form.errors


class TestProductForm:
    @pytest.mark.django_db
    def test_product_create(self):
        data = {
            "code": "test",
            "name": "Test",
            "short_name": "Short name test",
            "description": "Product description",
            "is_inventoried": True,
            "apply_iva": True,
            "apply_ice": False,
        }
        cost = 100
        cost_gross = round(cost * IVA_RATE, 5)
        form = ProductForm({**data, "cost_price": cost, "cost_price_gross": cost})
        product = form.save()

        assert form.is_valid() is True
        assert not form.errors
        assert isinstance(product, Product)
        assert data == model_to_dict(product, fields=data.keys())
        assert product.cost_price.amount == cost
        assert product.cost_price.gross_amount == cost_gross

    @pytest.mark.django_db
    def test_product_create_invalid(self):
        data = {
            "code": "test",
        }
        form = ProductForm(data)
        assert form.is_valid() is False
        assert form.errors
