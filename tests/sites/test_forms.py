import pytest
from django.forms.models import model_to_dict

from apps.sites.domain.enums import Emissions, Environments
from apps.sites.infra.forms import ConfigForm
from apps.sites.models import Config


class TestConfigForm:
    @pytest.mark.django_db
    def test_config_create(self):
        data = {
            "code": "1460000290001",
            "company_name": "test",
            "company_trade_name": "test",
            "company_main_address": "test",
            "company_branch_address": "test",
            "company_branch_code": "test",
            "company_sale_point_code": "test",
            "special_taxpayer_resolution": "test",
            "withholding_agent_resolution": "test",
            "company_accounting_required": False,
            "environment": str(Environments.TESTING),
            "emission_type": str(Emissions.NORMAL),
            "iva_percent": 12,
            "signature": None,
        }
        form = ConfigForm(data)

        assert form.is_valid() is True
        assert not form.errors

        config = form.save()

        assert isinstance(config, Config)
        assert data == model_to_dict(config, fields=("sri_config",)).get("sri_config")

    def test_config_create_invalid(self):
        data = {}
        form = ConfigForm(data)

        assert form.is_valid() is False
        assert form.errors
