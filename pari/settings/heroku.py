import dj_database_url

from .base import *  # noqa

DEBUG = False

COMPRESS_ENABLED = True

INSTALLED_APPS += (
    "storages",
)

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILES_STORAGE = 'pari.article.storage.CachedS3BotoStorage'
STATICFILES_STORAGE = DEFAULT_FILES_STORAGE
COMPRESS_STORAGE = DEFAULT_FILES_STORAGE

S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL
COMPRESS_URL = STATIC_URL
MEDIA_URL = STATIC_URL + "media/"

DATABASES['default'] = dj_database_url.config()
