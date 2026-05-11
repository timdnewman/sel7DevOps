import os

from .settings import *
from .settings import BASE_DIR

# The settings file for deployment

ALLOWED_HOSTS = [os.environ["WEBSITE_HOSTNAME"]]

CSRF_TRUSTED_ORIGINS = ["https://" + os.environ["WEBSITE_HOSTNAME"]]

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
    }
}
