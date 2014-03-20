from .base import *  # noqa


DEBUG = True

COMPRESS_ENABLED = False

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
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUND_CLOUD_CLIENT_ID = 'd129911dd3c35ec537c30a06990bd902'
