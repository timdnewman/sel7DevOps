import os

from .settings import *
from .settings import BASE_DIR

# The settings file for deployment

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-key")
hostname = os.environ["WEBSITE_HOSTNAME"]

ALLOWED_HOSTS = [hostname]

CSRF_TRUSTED_ORIGINS = ["https://" + hostname]

DEBUG = False

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CampressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

connection_string = os.environ["AZURE_POSTGRESQL_CONNECTIONSTRING"]

connection_params = {
    k: v for k, v in [pair.split("=") for pair in connection_string.split(" ")]
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": connection_params["dbname"],
        "HOST": connection_params["host"],
        "USER": connection_params["user"],
        "PASSWORD": connection_params["password"],
        "PORT": connection_params["port"] or 5432,
        "OPTIONS": {"sslmode": "require"},
    }
}
