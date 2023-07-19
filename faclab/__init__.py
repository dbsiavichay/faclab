from .cache import CacheService
from .celery import app as celery_app

__all__ = ["celery_app"]

cache = CacheService()
