import os

import dj_database_url

from .base import *  # noqa

DATABASES['default'] = dj_database_url.config()

DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))

COMPRESS_ENABLED = True

INSTALLED_APPS += (
    "django_extensions",
    # "storages",
)

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = 'pari.article.storage.ParallelS3Storage'
# STATICFILES_STORAGE = 'pari.article.storage.StaticRootS3BotoStorage'
# COMPRESS_STORAGE = DEFAULT_FILE_STORAGE

S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
# STATIC_URL = S3_URL
# COMPRESS_URL = STATIC_URL
MEDIA_URL = S3_URL + "media/"
# MEDIA_ROOT = ''

# STATICFILES_FINDERS += (
    # "django.contrib.staticfiles.finders.DefaultStorageFinder",
# )
