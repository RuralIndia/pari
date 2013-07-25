import os

from .prod import *  # noqa

DEBUG = bool(os.environ.get('DJANGO_DEBUG', 'true'))

HOSTNAME = "dev.ruralindiaonline.org"

ALLOWED_HOSTS.append(HOSTNAME)
SSL_FORCE_HOST = HOSTNAME

INSTALLED_APPS += (
    "debug_toolbar",
    "django_extensions",
)

MIDDLEWARE_CLASSES += (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}
