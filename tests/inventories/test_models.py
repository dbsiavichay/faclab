import pytest
from django.conf import settings
from django.forms.models import model_to_dict

from apps.inventories.models import Measure, Product, ProductCategory, Provider


class TestProductCategory:
    def test_settings(self):
        assert "apps.inventories" in settings.INSTALLED_APPS

    @pytest.mark.django_db
    def test_category_create(self):
        data = {
            "name": "Test",
        }
        category = ProductCategory.objects.create(**data)

        assert isinstance(category, ProductCategory)
        assert data == model_to_dict(category, fields=data.keys())


class TestProvider:
    @pytest.mark.django_db
    def test_provider_create(self):
        data = {
            "code": "test",
            "bussiness_name": "Test",
            "contact_name": "Test",
            "phone": "0912334533",
            "email": "test@test.com",
        }
        provider = Provider.objects.create(**data)

        assert isinstance(provider, Provider)
        assert data == model_to_dict(provider, fields=data.keys())


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
