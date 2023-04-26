from .models import Config


class SRIConfig:
    code = None
    company_name = None
    trade_name = None
    main_address = None
    company_address = None
    company_code = None
    company_point_sale_code = None
    special_taxpayer_resolution = None
    withholding_agent_resolution = None
    accounting_required = None
    environment = None
    emission = None
    iva_percent = None
    iva_rate = None
    iva_factor = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.iva_rate = self.iva_percent / 100
        self.iva_factor = (self.iva_percent / 100) + 1


class SRIConfigService:
    @classmethod
    def get_sri_config(cls):
        config = Config.objects.first()
        sri_config = SRIConfig(**config.sri_config)

        return sri_config
