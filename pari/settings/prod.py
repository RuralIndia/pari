import os

from .base import *  # noqa

HOSTNAME = "www.ruralindiaonline.org"

ALLOWED_HOSTS.append(HOSTNAME)
SSL_FORCE_HOST = HOSTNAME


SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pari',
        'USER': 'postgres',
        'PASSWORD': '!abcd1234',
        'HOST': 'localhost'
    }
}

DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))

COMPRESS_ENABLED = True

DEFAULT_FILE_STORAGE = 'pari.article.storage.ParallelS3Storage'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
