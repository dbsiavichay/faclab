from .cache import CacheService
from .celery import app as celery_app

# from .containers import ApplicationContainer

__all__ = ["celery_app"]

cache = CacheService()

# container = ApplicationContainer()
