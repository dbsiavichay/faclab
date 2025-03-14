"""
Django settings for faclab project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

import environ

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = []

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LIBRARY_APPS = [
    "minio_storage",
    "rest_framework",
    "simple_menu",
    "viewpack",
    "widget_tweaks",
]

LOCAL_APPS = [
    "apps.account",
    "apps.core",
    "apps.purchase",
    "apps.inventory",
    "apps.sale",
]

INSTALLED_APPS = DJANGO_APPS + LIBRARY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "faclab.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "faclab.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {"default": env.db()}

MIGRATION_MODULES = {
    "account": "apps.account.infra.migrations",
    "core": "apps.core.infra.migrations",
    "inventory": "apps.inventory.infra.migrations",
    "purchase": "apps.purchase.infra.migrations",
    "sale": "apps.sale.infra.migrations",
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # Noqa E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # Noqa E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # Noqa E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # Noqa E501
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "es-EC"
TIME_ZONE = "America/Guayaquil"
LOCALE_PATHS = [BASE_DIR / "locale"]
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Custom user model
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#substituting-a-custom-user-model

AUTH_USER_MODEL = "account.User"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

# Redis cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Django select2
SELECT2_CACHE_BACKEND = "default"
SELECT2_CSS = ["vendors/select2/select2.css"]

# Celery
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env("CELERY_REDIS_URL")


# SRI
KEYTOOL_COMMAND = env("KEYTOOL_COMMAND")
SRI_GET_TAXPAYERS_WS = env("SRI_GET_TAXPAYERS_WS")

SRI_PACKAGE = {
    "VOUCHER_WS": "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl",  # NOQA : E501
    "AUTHORIZATION_WS": "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl",  # NOQA : E501
    "TIME_ZONE": TIME_ZONE,
}

# SEALIFY
SEALIFY_BASE_URL = env("SEALIFY_BASE_URL", default="http://localhost:3000")

# KAFKA
KAFKA_BROKER_URL = env(
    "KAFKA_BROKER_URL", default="kafka:9092"
)  # Nombre del contenedor
KAFKA_TOPIC = "invoices"
