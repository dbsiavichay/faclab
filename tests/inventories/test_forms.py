import pytest
from django.forms.models import model_to_dict

from apps.inventories.forms import ProductForm
from apps.inventories.models import Product

IVA_RATE = 1.12


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
