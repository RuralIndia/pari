import os

from .base import *  # noqa

HOSTNAME = "www.ruralindiaonline.org"

ALLOWED_HOSTS.append(HOSTNAME)
SSL_FORCE_HOST = HOSTNAME

ANALYTICS_ENABLED = True

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ["DJANGO_DB_NAME"],
        'USER': os.environ["DJANGO_DB_USER"],
        'PASSWORD': os.environ["DJANGO_DB_PASSWORD"],
        'HOST': 'localhost'
    }
}


RECAPTCHA_PUBLIC_KEY = os.environ["DJANGO_RECAPTCHA_PUBLIC_KEY"]
RECAPTCHA_PRIVATE_KEY = os.environ["DJANGO_RECAPTCHA_PRIVATE_KEY"]

DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))

COMPRESS_ENABLED = True

DEFAULT_FILE_STORAGE = 'pari.article.storage.ParallelS3Storage'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

INSTALLED_APPS += (
    "djrill",
)

# Email Settings
MANDRILL_API_KEY = os.environ["DJANGO_MANDRILL_API_KEY"]
DEFAULT_FROM_EMAIL = "do-no-reply@ruralindiaonline.org"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
