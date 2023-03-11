from django.utils.module_loading import autodiscover_modules

from viewpack.base import ModelPack
from viewpack.services.packs import packs

__all__ = ["packs", "ModelPack"]

default_app_config = "viewpack.apps.ViewPackConfig"


def autodiscover():
    autodiscover_modules("packs")
