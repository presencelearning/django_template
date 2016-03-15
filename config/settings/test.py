# -*- coding: utf-8 -*-
'''
Production Configurations

- Use djangosecure
'''
from __future__ import absolute_import, unicode_literals


from .common import *  # noqa

# django-secure
# ------------------------------------------------------------------------------
INSTALLED_APPS += ("djangosecure", )

MIDDLEWARE_CLASSES = (
    # Make sure djangosecure.middleware.SecurityMiddleware is listed first
    'djangosecure.middleware.SecurityMiddleware',
) + MIDDLEWARE_CLASSES

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_FRAME_DENY = env.bool("DJANGO_SECURE_FRAME_DENY", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [".presencetest.com"]
# END SITE CONFIGURATION

INSTALLED_APPS += ("gunicorn", )


CELERY_ALWAYS_EAGER = False

RAVEN_CONFIG = {
    'dsn': 'https://43d81b91dc29489fbd2ded5844a14509:4dee1a4c284b4cb3bb45ca4f841d2805@app.getsentry.com/13216', # DSN for test
    'release': env('DEPLOYED_SHA', default='')
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'celery': {
            'handlers'    : ['console'],
            'propagate'    : True,
        },
        '': {
            'handlers': ['sentry'],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}

# Your production stuff: Below this line define 3rd party library settings
