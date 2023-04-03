import pytest
from django.conf import settings
from django.forms.models import model_to_dict

from apps.warehouses.models import Measure, Product, ProductCategory


class TestProductCategory:
    def test_settings(self):
        assert "apps.warehouses" in settings.INSTALLED_APPS

    @pytest.mark.django_db
    def test_category_create(self):
        data = {
            "name": "Test",
        }
        category = ProductCategory.objects.create(**data)

        assert isinstance(category, ProductCategory)
        assert data == model_to_dict(category, fields=data.keys())


class TestMeasure:
    @pytest.mark.django_db
    def test_measure_create(self):
        data = {"code": "test", "name": "Test"}
        measure = Measure.objects.create(**data)

        assert isinstance(measure, Measure)
        assert data == model_to_dict(measure, fields=data.keys())


class TestProduct:
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
        product = Product.objects.create(**data)

        assert isinstance(product, Product)
        assert data == model_to_dict(product, fields=data.keys())
