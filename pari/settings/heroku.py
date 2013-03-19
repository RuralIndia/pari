import dj_database_url

from .base import *  # noqa


DEBUG = True

DATABASES['default'] = dj_database_url.config()
