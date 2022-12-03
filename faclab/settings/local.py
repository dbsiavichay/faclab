"""Base development settings."""

from .base import *
from .base import env

# Security
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="PB3aGvTmCkzaLGRAxDc3aMayKTPTDd5usT8gw4pCmKOk5AlJjh12pTrnNgQyOHCH",
)
#ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", ["*"])
