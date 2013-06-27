from .base import *  # noqa


DEBUG = True

COMPRESS_ENABLED = False

ALLOWED_HOSTS.append("dev.ruralindiaonline.org")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": PROJECT_ROOT.child("dev.db"),
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
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
