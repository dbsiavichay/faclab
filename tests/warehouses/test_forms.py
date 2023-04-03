import pytest
from django.forms.models import model_to_dict

from apps.warehouses.forms import ProductForm
from apps.warehouses.models import Product


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
        form = ProductForm(data)
        product = form.save()

        assert form.is_valid() is True
        assert not form.errors
        assert isinstance(product, Product)
        assert data == model_to_dict(product, fields=data.keys())

    @pytest.mark.django_db
    def test_product_create_invalid(self):
        data = {
            "code": "test",
        }
        form = ProductForm(data)
        assert form.is_valid() is False
        assert form.errors
