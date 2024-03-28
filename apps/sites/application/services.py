from faclab import cache

SRI_CONFIG_CACHE_KEY = "sri_config"


class SRIConfig:
    id = None
    iva_percent = None
    signature = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def iva_rate(self):
        return self.iva_percent / 100 if self.iva_percent else None

    @property
    def iva_factor(self):
        return (self.iva_percent / 100) + 1 if self.iva_percent else None


class SRIConfigService:
    @classmethod
    # @cache.set_cache(SRI_CONFIG_CACHE_KEY, [])
    def get_sri_config(cls):
        from apps.sites.models import Config

        config = Config.objects.first()
        data_config = {"id": config.id, **config.sri_config} if config else {}
        sri_config = SRIConfig(**data_config)

        return sri_config

    @classmethod
    def delete_sri_cache_config(cls):
        cache.delete(SRI_CONFIG_CACHE_KEY)


class ConfigService:
    # @cache.set_cache(SRI_CONFIG_CACHE_KEY, [])
    def get_config_object(self):
        from apps.sites.models import Config

        return Config.objects.first()

    def get_sri_config(self) -> SRIConfig:
        config = self.get_config_object()
        data_config = {"id": config.id, **config.sri_config} if config else {}
        sri_config = SRIConfig(**data_config)

        return sri_config

    def delete_sri_cache_config(self) -> None:
        cache.delete(SRI_CONFIG_CACHE_KEY)
