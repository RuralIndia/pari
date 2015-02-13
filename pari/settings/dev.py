import os
from .base import *  # noqa


DEBUG = bool(os.environ.get('DJANGO_DEBUG', 'true'))

COMPRESS_ENABLED = False

ALLOWED_HOSTS.append("dev.ruralindiaonline.org")

COMMENTS_DISQUS_SHORTNAME = "twpari"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pari',
        'USER': 'pari',
        'PASSWORD': 'pari',
        'HOST': 'localhost'
    }
}

INSTALLED_APPS += (
    "django_nose",
    "debug_toolbar",
    "django_extensions",
)

MIDDLEWARE_CLASSES += (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DEFAULT_FILE_STORAGE = 'pari.article.storage.ParallelS3Storage'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://localhost:9200',
        'INDEX_NAME': 'haystack',
    },
}

# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
