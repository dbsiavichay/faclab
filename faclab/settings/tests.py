"""Base tests settings."""

from .base import *  # Noqa F403
from .base import DATABASES

DATABASES["default"]["NAME"] = "faclab_test"
