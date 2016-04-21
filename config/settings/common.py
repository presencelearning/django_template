# -*- coding: utf-8 -*-
"""
Django settings for {{ project_name }} project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from __future__ import absolute_import, unicode_literals

import environ
import datetime
import os

from django.core.urlresolvers import reverse_lazy

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path('{{ project_name }}')

env = environ.Env()

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: The default key only used for development and testing.
SECRET_KEY = env.str('DJANGO_SECRET_KEY', default='')

# This ensures that Django will be able to detect a secure connection
# properly.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CACHE
# ------------------------------------------------------------------------------
# read from CACHE_URL, see https://github.com/ghickman/django-cache-url
CACHES = {
    'default': env.cache(default='locmemcache://'),
}

for cache in CACHES:
    if CACHES[cache]['BACKEND'] == 'django_redis.cache.RedisCache':
        CACHES[cache]['OPTIONS'] = {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,  # mimics memcache behavior.
                                        # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        }

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework_swagger',
    'raven.contrib.django.raven_compat',
    'pl.service',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'plauth',
    'hello_world', # example to be removed
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    # Make sure djangosecure.middleware.SecurityMiddleware is listed first
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': '{{ project_name }}.contrib.sites.migrations'
}

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
                         default='auth <noreply@presencelearning.com>')
EMAIL_URL = env.email_url(default='consolemail://')
EMAIL_HOST = EMAIL_URL.get('EMAIL_HOST')
EMAIL_HOST_USER = EMAIL_URL.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = EMAIL_URL.get('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = EMAIL_URL.get('EMAIL_BACKEND')
EMAIL_FILE_PATH = EMAIL_URL.get('EMAIL_FILE_PATH')
EMAIL_PORT = EMAIL_URL.get('EMAIL_PORT')
EMAIL_USE_TLS = EMAIL_URL.get('EMAIL_USE_TLS')
EMAIL_USE_SSL = EMAIL_URL.get('EMAIL_USE_SSL')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Sandy Lerman', 'sandy@presencelearning.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db(default='mysql://learning:learning@localhost:3306/{{ project_name }}'), # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
}

for db in DATABASES:
    DATABASES[db]['OPTIONS'] = {
        'init_command': 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED'
    }

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('uploaded_files'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'

# AUTHENTICATION CONFIGURATION AND API
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'plauth.User'
LOGIN_URL = reverse_lazy('oidc_login')
LOGIN_REDIRECT_URL = '/'
DEPLOYED_SHA = env('DEPLOYED_SHA', default='')
OIDC_CLIENT_ID = env('OIDC_CLIENT_ID', default=DEPLOYED_SHA)
OIDC_CLIENT_SECRET = env('OIDC_CLIENT_SECRET', default=DEPLOYED_SHA)
OIDC_SCOPES = ('openid', 'preferred_username', 'email', 'profile')
OIDC_REDIRECT_URI = env('OIDC_REDIRECT_URI', default='https://localhost:8000/oidc/callback/'.format(DEPLOYED_SHA))
OIDC_PUBLIC_KEY = { # found at https://login.presencetest.com/openid/jwks/
    "n": "2_S5pnyUjy0xlLE0IkfR-uBiCdFNaNu3aF2IeLNP_bW7YXLdl-gYIQZWaEXk9vnf6IKm4Ky5q6SaDPSRrGFi8jTrip3ka-oW4HRFtMcHqFcT6etaeQhBTHNjxOXXxBBh0C8FelkQ8-hsO9YZlwje38eYYhlnqyFJ3n6C83kgDUvvCI0Q04OrX3GvxNkGrL5IjwXHii5Pr9DcLJyYpmLY4V3eILbCpTcU9HOzJ8K2EWar2W0_jFVIOYca-Bf5PU2iZM6PQCEnBUFPvc7PwVVPj_HV_pUQVmTx1iI7FedufQrC2vG0KlUGJO4jVcH3n5IEfx8R0kTe0OXtU768KtgnsWPvkBiMOz7RUphkMXXZ8ZC4VCin90fGARcUCM3eV5OYqYIJooqz5DqhSjd7Y2NXhvIjDgqiCrqhIweHXoZBmvRQ6_6o_6Y5nBngT8_F-0gIHRN-eCFlnf16drlZasHqoecVQi4GfFuHU1e3zMA0wwshSwL4zEkTc8qXoT3Kp4xd9mayA1GubmZRXjN5S_IbLGM8aiSqlt5tJS3NEy4uUnLi5m5RoL1ljidDVcpNwZTbyZhqlM-18izFRPbzJjvIpDwn7EU_NnzYLxXagahK5DfG1zLQX6p563NS0zNSDZbqT6syfV1fHVm4s77ZDqGD8_RyCODZfmf9Z_CG2wErjDU",
    "e": "AQAB",
    "kid": "7058a84d74a4ae3423995e0ec051f908",
    "alg": "RS256",
    "use": "sig",
    "kty": "RSA"
}
OIDC_STATE_COOKIE_DOMAIN = '.live.presencetest.com'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
JWT_AUTH = {
    'JWT_DECODE_HANDLER': 'pl.jwt.handler.jwt_decode_handler',
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': lambda p: p['sub'],
}

SWAGGER_SETTINGS = {
    'api_version': '1.0',
}

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

########## CELERY
from kombu import Exchange, Queue
BROKER_URL = env("CELERY_BROKER_URL", default='amqp://guest:guest@localhost:5672/')
BROKER_POOL_LIMIT = 0 # for ELB
BROKER_HEARTBEAT = 30
CELERY_TASK_SERIALIZER = "json"
CELERY_DEFAULT_QUEUE = 'default_{{ project_name }}'
CELERY_QUEUES = (
    Queue('default_{{ project_name }}', Exchange('default_{{ project_name }}'), routing_key='default_{{ project_name }}'),
)
CELERY_TIMEZONE = 'UTC'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_ALWAYS_EAGER = True

BUS_URL = env("BUS_URL", default='amqp://guest:guest@localhost:5672/bus')
BUS_APP_ID = '{{ project_name }}'

########## TESTS

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_VERBOSE = True
TEST_OUTPUT_DESCRIPTIONS = True
TEST_OUTPUT_DIR = 'test_reports'

# Your common stuff: Below this line define 3rd party library settings
