import pytest
from django.conf import settings
from django.forms.models import model_to_dict

from apps.sites.models import Config


class TestConfig:
    def test_settings(self):
        assert "apps.sites" in settings.INSTALLED_APPS

    @pytest.mark.django_db
    def test_config_create(self):
        data = {"sri_config": {"name": "test"}}
        config = Config.objects.create(**data)

        assert isinstance(config, Config)
        assert isinstance(config.sri_config, dict)
        assert data == model_to_dict(config, fields=data.keys())
