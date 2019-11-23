"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SETTINGS_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


class _RememberKeyErrorsDict(dict):
    """
    Dictionary that remembers key errors instead of instantly throwing except
    will throw missing keys exceptions when fail_if_missing_keys is called so do remember to call that
    """

    def __init__(self, message, *args, **kwargs):
        super(_RememberKeyErrorsDict, self).__init__(*args, **kwargs)
        self._missing_keys = []
        self._message = message

    def __missing__(self, key):
        self._missing_keys.append(key)

    def fail_if_missing_keys(self):
        if self._missing_keys:
            raise KeyError(f"{self._message}: {', '.join(self._missing_keys)}")


ALLOWED_HOSTS = ["*"]
with open(os.path.join(SETTINGS_DIR, "config.json")) as json_file:
    _CONFIG = _RememberKeyErrorsDict("Following keys are missing from config.json", json.load(json_file))

SECRET_KEY = _CONFIG["SECRET_KEY"]

FRONTEND_URL = _CONFIG["FRONTEND_URL"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "corsheaders",
    "rest_framework",
    "rest_api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "corsheaders.middleware.CorsMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "rest_api.utils.custom_exception_handlers.HandleExceptionMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.SessionAuthentication",),
    "EXCEPTION_HANDLER": "rest_api.utils.custom_exception_handlers.custom_exception_handler",
}
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "backend.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3")}}
if _CONFIG.get("DATABASE_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "backend",
            "USER": "backend",
            "PASSWORD": _CONFIG.get("DATABASE_PASSWORD"),
            "HOST": _CONFIG.get("DATABASE_HOST"),
            "PORT": "5432",
        }
    }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] - [{levelname}] - [{name}.{funcName}:{lineno}] : {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        }
    },
    "handlers": {"console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "verbose"}},
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "backend": {"handlers": ["console"], "level": "INFO"},
    },
}
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# Openid Connect config
# NOTE that running oidc locally is possible by using a 'prod' client and redirecting
# the callback url to localhost inside your browser,
LOGOUT_REDIRECT_URL = "/"
# CSRF config
CSRF_COOKIE_DOMAIN = _CONFIG.get("CSRF_COOKIE_DOMAIN", "localhost")
CSRF_TRUSTED_ORIGINS = ["localhost", "127.0.0.1", CSRF_COOKIE_DOMAIN]

CSRF_COOKIE_SECURE = _CONFIG["IS_PROD"]  # Force the cookie to transit via HTTPS in prod
CSRF_USE_SESSIONS = False  # False then Angular can use it
CSRF_COOKIE_HTTPONLY = False
# SSL config
SECURE_SSL_REDIRECT = _CONFIG["IS_PROD"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# CORS config
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    "x-requested-with",
    "x-csrftoken",
    "content-type",
    "accept",
    "origin",
    "authorization",
    "as-standard-user",
)

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "/static"

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"
if TESTING:
    import logging

    logging.disable(logging.CRITICAL)
    DEBUG = False
    TEMPLATE_DEBUG = False
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
    MIDDLEWARE_CLASSES = [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ]
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
_CONFIG.fail_if_missing_keys()
