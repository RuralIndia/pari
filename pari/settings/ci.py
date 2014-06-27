from .base import *  # noqa


DEBUG = True

COMPRESS_ENABLED = False

SOUTH_TESTS_MIGRATE = False

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

SOUND_CLOUD_CLIENT_SECRET = '4413528c126613cd9535b318241ed24d'
SOUND_CLOUD_CLIENT_ID = 'f63f72df4a0eb0606e3c7aaf12d8241b'
SOUND_CLOUD_USERNAME = 'arvindram03@gmail.com'
SOUND_CLOUD_PASSWORD = 'getonwithit'
