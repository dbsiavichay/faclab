"""
WSGI config for faclab project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from .containers import build_container

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "faclab.settings")

application = get_wsgi_application()

build_container()
