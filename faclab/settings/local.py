"""Base development settings."""

from .base import *  # Noqa F403
from .base import env

# from .storage import *  # Noqa F403

# Security
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="PB3aGvTmCkzaLGRAxDc3aMayKTPTDd5usT8gw4pCmKOk5AlJjh12pTrnNgQyOHCH",
)
