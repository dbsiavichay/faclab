import pytest
from django.forms.models import model_to_dict

from apps.sites.forms import ConfigForm
from apps.sites.models import Config


class TestConfigForm:
    @pytest.mark.django_db
    def test_config_create(self):
        data = {
            "code": "1460000290001",
            "company_name": "test",
            "trade_name": "test",
            "main_address": "test",
            "company_address": "test",
            "company_code": "test",
            "company_point_sale_code": "test",
            "special_taxpayer_resolution": "test",
            "withholding_agent_resolution": "test",
            "accounting_required": False,
        }
        form = ConfigForm(data)
        config = form.save()

        assert form.is_valid() is True
        assert not form.errors
        assert isinstance(config, Config)
        assert data == model_to_dict(config, fields=("sri_config",)).get("sri_config")

    def test_config_create_invalid(self):
        data = {}
        form = ConfigForm(data)

        assert form.is_valid() is False
        assert form.errors
