"""
WSGI config for faclab project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from . import settings
from .containers import ApplicationContainer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "faclab.settings")

application = get_wsgi_application()

container = ApplicationContainer()
container.config.from_dict(settings.__dict__)

container.wire(
    modules=[
        "apps.core.application.main_menu",
        "apps.core.infra.forms",
        "apps.core.infra.repositories",
        "apps.sale.infra.forms",
        "apps.sri.application.services",
    ]
)
