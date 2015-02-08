from django.utils.translation import ugettext_lazy as _
from unipath import Path
import os

######################
# MEZZANINE SETTINGS #
######################

# The following settings are already defined with default values in
# the ``defaults.py`` module within each of Mezzanine's apps, but are
# common enough to be put here, commented out, for convenient
# overriding. Please consult the settings documentation for a full list
# of settings Mezzanine implements:
# http://mezzanine.jupo.org/docs/configuration.html#default-settings

# Controls the ordering and grouping of the admin menu.

ADMIN_MENU_ORDER = (
    (_("Content"),
     ("pages.Page", "article.Article", "article.Author", "article.Location", "article.Category", "article.Type",
      "album.Album", "album.ImageCollection", "faces.District", "faces.Face", "resources.Resource", "resources.Factoid",
      "contribution.Contribution",
      (_("Media Library"), "fb_browse"),)),
    (_("Site"), ("sites.Site", "redirects.Redirect", "conf.Setting")),
    (_("Users"), ("auth.User", "auth.Group",)),
)

# A three item sequence, each containing a sequence of template tags
# used to render the admin dashboard.

DASHBOARD_TAGS = (
    ("mezzanine_tags.app_list",),
    ("comment_tags.recent_comments",),
    ("mezzanine_tags.recent_actions",),
)

# A sequence of templates used by the ``page_menu`` template tag. Each
# item in the sequence is a three item sequence, containing a unique ID
# for the template, a label for the template, and the template path.
# These templates are then available for selection when editing which
# menus a page should appear in. Note that if a menu template is used
# that doesn't appear in this setting, all pages will appear in it.

# PAGE_MENU_TEMPLATES = (
#     (1, "Top navigation bar", "pages/menus/dropdown.html"),
#     (2, "Left-hand tree", "pages/menus/tree.html"),
#     (3, "Footer", "pages/menus/footer.html"),
# )

# A sequence of fields that will be injected into Mezzanine's (or any
# library's) models. Each item in the sequence is a four item sequence.
# The first two items are the dotted path to the model and its field
# name to be added, and the dotted path to the field class to use for
# the field. The third and fourth items are a sequence of positional
# args and a dictionary of keyword args, to use when creating the
# field instance. When specifying the field class, the path
# ``django.models.db.`` can be omitted for regular Django model fields.
#
EXTRA_MODEL_FIELDS = (
    (
        "mezzanine.pages.models.Link.html_class",
        "CharField",
        ("HTML Class",),
        {"max_length": 100, "blank": True, "null": True, "default": ""},
    ),
)

FORMS_EXTRA_FIELDS = (
    (99,
     "pari.contribution.fields.CaptchaField",
     "Captcha"),
    (98,
     "pari.contribution.fields.ContributionsField",
     "Contributions"),
)
# Setting to turn on featured images for blog posts. Defaults to False.
#
BLOG_USE_FEATURED_IMAGE = True

# If True, the south application will be automatically added to the
# INSTALLED_APPS setting.
USE_SOUTH = True

BLOG_SLUG = "article"

GEOPOSITION_DEFAULT_ZOOM = 5

GEOPOSITION_DEFAULT_CENTRE = (21.77, 78.87,)

DEVICE_USER_AGENTS = (
    ("mobile", ("Android", "BlackBerry", "iPhone", "Windows Phone")),
    ("desktop", ("Windows", "Macintosh", "Linux")),
)

RICHTEXT_WIDGET_CLASS = 'pari.article.forms.TinyMceWidget'

RICHTEXT_FILTERS = (
    'pari.article.rich_text_filter.article_content_filter',
)

FORMS_USE_HTML5 = True
RECAPTCHA_USE_SSL = True

RECAPTCHA_PUBLIC_KEY = '6LdQguISAAAAAPNt_0pFGdVXubB1MJn9J-im-3KD'
RECAPTCHA_PRIVATE_KEY = '6LdQguISAAAAAJgLhCqkCNbjkhG1J9_2Q2kLEsAO'

AUTH_PROFILE_MODULE = "user.Profile"
ACCOUNTS_VERIFICATION_REQUIRED = True

SSL_FORCE_URL_PREFIXES = ("/admin", "/account", "/donate", "/asset_proxy")
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

SEARCH_MODEL_CHOICES = (
    "pages.Page",
    "blog.BlogPost",
    "article.Article",
    "article.Location",
    "article.Category",
    "article.Author",
    "album.Album",
    "album.AlbumImage",
    "resources.Resource",
    "resources.Factoid",
    "contribution.Contribution",
)

########################
# MAIN DJANGO SETTINGS #
########################

# People who get code error notifications.
# In the format (('Full Name', 'email@example.com'),
#                ('Full Name', 'anotheremail@example.com'))
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Asia/Calcutta"

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
# production. Best set to ``True`` in local_settings.py
DEBUG = False

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = "ddd8bef6-495d-4925-ae37-1f13f9fe679404584f84-f4db-4f15-a096-72f545486dc6a72928ae-ef6b-486a-86a0-d511c82c5534"

# Tuple of IP addresses, as strings, that:
#   * See debug comments, when DEBUG is true
#   * Receive x-headers
INTERNAL_IPS = ("127.0.0.1",)

ALLOWED_HOSTS = ["localhost"]


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
    "django.template.loaders.eggs.Loader",
)

AUTHENTICATION_BACKENDS = ("mezzanine.core.auth_backends.MezzanineBackend",)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "dajaxice.finders.DajaxiceFinder",
    "compressor.finders.CompressorFinder",
    # "django.contrib.staticfiles.finders.DefaultStorageFinder",
)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/typescript', 'tsc {infile} --out {outfile}'),
)

COMPRESS_ENABLED = True

COMPRESS_PARSER = 'compressor.parser.HtmlParser'

WSGI_APPLICATION = "pari.wsgi.application"

#############
# DATABASES #
#############

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.",
        # DB name or path to database file if using sqlite3.
        "NAME": "",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}


#########
# PATHS #
#########

# Full filesystem path to the project.
PROJECT_ROOT = Path(__file__).ancestor(2)

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_ROOT.name

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_ROOT.child('static')

COMPRESS_ROOT = STATIC_ROOT

# STATICFILES_DIRS = (PROJECT_ROOT.child('static'),)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = STATIC_ROOT.child('media')

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME

# Put strings here, like "/home/html/django_templates"
# or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (PROJECT_ROOT.child("templates"), )

FIXTURE_DIRS = PROJECT_ROOT.child("fixtures")


################
# APPLICATIONS #
################

INSTALLED_APPS = (
    "modeltranslation",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",

    # Mezzanine CMS
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.forms",
    "mezzanine.blog",
    "mezzanine.pages",
    "mezzanine.galleries",
    "mezzanine.twitter",
    "mezzanine.accounts",
    # "mezzanine.mobile",

    "south",
    "geoposition",
    "rest_framework",
    "compressor",
    'dajaxice',
    'dajax',
    "captcha",
    # Custom
    "pari.article",
    "pari.map",
    "pari.album",
    "pari.contribution",
    "pari.resources",
    "pari.user",
    "pari.search",
    "pari.faces",
    "pari.news",
    "pari.thirdparty"
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "mezzanine.conf.context_processors.settings",
    "mezzanine.pages.context_processors.page",
    "pari.article.context_processors.types",
    "pari.article.context_processors.sites",
)

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    "django.middleware.gzip.GZipMiddleware",
    "mezzanine.core.middleware.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
)

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

# SoundCloud credentials
SOUND_CLOUD_CLIENT_SECRET = os.environ.get('SOUND_CLOUD_CLIENT_SECRET', 'true')
SOUND_CLOUD_CLIENT_ID = os.environ.get('SOUND_CLOUD_CLIENT_ID', 'true')
SOUND_CLOUD_USERNAME = os.environ.get('SOUND_CLOUD_USERNAME', 'true')
SOUND_CLOUD_PASSWORD = os.environ.get('SOUND_CLOUD_PASSWORD', 'true')

# Translation related settings
# Language codes taken from https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
gettext = lambda s: s
LANGUAGES = (
    ("en", gettext("English")),
    ("hi", gettext("Hindi")),
    ("mr", gettext("Marathi")),
    ("te", gettext("Telugu")),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
#########################
# OPTIONAL APPLICATIONS #
#########################

OPTIONAL_APPS = (
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}
NEVERCACHE_KEY = ""

TESTING = True

###################
# DEPLOY SETTINGS #
###################

# These settings are used by the default fabfile.py provided.
# Check fabfile.py for defaults.

# FABRIC = {
#     "SSH_USER": "", # SSH username
#     "SSH_PASS":  "", # SSH password (consider key-based authentication)
#     "SSH_KEY_PATH":  "", # Local path to SSH key file, for key-based auth
#     "HOSTS": [], # List of hosts to deploy to
#     "VIRTUALENV_HOME":  "", # Absolute remote path for virtualenvs
#     "PROJECT_NAME": "", # Unique identifier for project
#     "REQUIREMENTS_PATH": "", # Path to pip requirements, relative to project
#     "GUNICORN_PORT": 8000, # Port gunicorn will listen on
#     "LOCALE": "en_US.UTF-8", # Should end with ".UTF-8"
#     "LIVE_HOSTNAME": "www.example.com", # Host for public site.
#     "REPO_URL": "", # Git or Mercurial remote repo URL for the project
#     "DB_PASS": "", # Live database password
#     "ADMIN_PASS": "", # Live admin user password
# }

####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
