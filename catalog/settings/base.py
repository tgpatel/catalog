"""
Django settings for catalog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from __future__ import print_function

import os
import logging
import sys

DEBUG = False
TEMPLATE_DEBUG = DEBUG

USE_TZ = True

# tweaking standard BASE_DIR because we're in the settings subdirectory.
BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

DEFAULT_FROM_EMAIL = 'vcweb@asu.edu'
EMAIL_HOST = 'smtp.asu.edu'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ALLOWED_HOSTS = ('.asu.edu', 'localhost',)
ADMINS = (
    ('Allen Lee', 'allen.lee@asu.edu'),
)
MANAGERS = ADMINS

DATA_DIR = 'data'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_DIR, 'catalog.sqlite3'),
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'comses_catalog',
        'USER': 'catalog',
        'PASSWORD': '',
    }
}

# Haystack settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr'
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Phoenix'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.  Default is '/static/admin/'
# ADMIN_MEDIA_PREFIX = '/static/admin/'

# Salt used to generate token (SALT can remain public unlike SECRET_KEY)
SALT = '48&6uv*x'

# Zotero API Key
ZOTERO_API_KEY = None


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.debug",
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    "django.core.context_processors.tz",
    'django.contrib.messages.context_processors.messages',
    'dealer.contrib.django.context_processor',
)

MIDDLEWARE_CLASSES = (
#    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
#    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'catalog.urls'

# cookie storage vs session storage of django messages
# MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
#    'raven.contrib.django.raven_compat',
    'kronos',
    'bootstrap3',
    'haystack',
    'rest_framework',
    'django_extensions'
)


CATALOG_APPS = ('catalog.core',)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CATALOG_APPS

# activation window
ACCOUNT_ACTIVATION_DAYS = 30

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/catalog/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'catalog', 'static').replace('\\', '/'),)

# Media file configuration (for user uploads etc) ####

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/catalog/uploads'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'https://catalog.comses.net/uploads/'


def is_accessible(directory_path):
    return os.path.isdir(directory_path) and os.access(directory_path, os.W_OK | os.X_OK)

LOG_DIRECTORY = '/opt/catalog/logs'

if not is_accessible(LOG_DIRECTORY):
    try:
        os.makedirs(LOG_DIRECTORY)
    except OSError:
        print("Unable to create absolute log directory at %s, setting to relative path logs instead" % LOG_DIRECTORY, file=sys.stderr)
        LOG_DIRECTORY = 'logs'
        if not is_accessible(LOG_DIRECTORY):
            try:
                os.makedirs(LOG_DIRECTORY)
            except OSError:
                print("Couldn't create any log directory, startup will fail", file=sys.stderr)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry', 'catalog.file'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s [%(name)s|%(funcName)s:%(lineno)d] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'formatter': 'verbose',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'catalog.file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIRECTORY, 'catalog.log'),
            'backupCount': 6,
            'maxBytes': 10000000,
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'catalog': {
            'level': 'DEBUG',
            'handlers': ['catalog.file', 'console'],
            'propagate': False,
        },
    }
}

# reset in local.py to enable more verbose logging (e.g.,
# DISABLED_TEST_LOGLEVEL = logging.NOTSET)
DISABLED_TEST_LOGLEVEL = logging.WARNING

# TEST_RUNNER = 'catalog.core.tests.runner.CatalogTestRunner'

# revision reporting support using dealer
DEALER_TYPE = 'git'
DEALER_SILENT = True
DEALER_BACKENDS = ('git', 'mercurial')
DEALER_PATH = BASE_DIR

# DJANGO REST Framework's Pagination settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15
}
