import os

from .prod import *  # noqa

DEBUG = bool(os.environ.get('DJANGO_DEBUG', 'true'))

ALLOWED_HOSTS.append("dev.ruralindiaonline.org")

INSTALLED_APPS += (
    "debug_toolbar",
    "django_extensions",
)

MIDDLEWARE_CLASSES += (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}
