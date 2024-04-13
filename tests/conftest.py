import pytest

from apps.sites.domain.enums import Emissions, Environments
from apps.sites.models import Config


@pytest.fixture
def sri_config(db):
    config = {
        "code": "1460000290001",
        "company_name": "test",
        "company_trade_name": "test",
        "company_main_address": "test",
        "company_branch_address": "test",
        "company_branch_code": "001",
        "company_sale_point_code": "001",
        "special_taxpayer_resolution": "test",
        "withholding_agent_resolution": "test",
        "company_accounting_required": False,
        "environment": str(Environments.TESTING),
        "emission": str(Emissions.NORMAL),
        "iva_percent": 12,
    }
    data = {"sri_config": config}

    return Config.objects.create(**data)
