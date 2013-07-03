import os

from .base import *  # noqa

ALLOWED_HOSTS.append("dev.ruralindiaonline.org")

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

#Memcached settings
MIDDLEWARE_CLASSES += (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
        }
}
