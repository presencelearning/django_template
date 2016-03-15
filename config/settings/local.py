# -*- coding: utf-8 -*-
'''
Local settings

- Run in Debug mode
- Use console backend for emails
- Add django-extensions as app
'''

from .common import *  # noqa

SECRET_KEY = 'foo'

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions', )

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# TEMPLATES
# ------------------------------------------------------------------------------
DEFAULT_APP_TEMPLATE = 'https://github.com/presencelearning/django_app_template/zipball/master'
DEFAULT_APP_TEMPLATE_EXTENSIONS = ['py', 'rst,py']

OIDC_CLIENT_ID = 'localhost8000'
OIDC_CLIENT_SECRET = 'snxVpnNYnrrP2ReYAkGKYkQXcp42fkbvX5WfbTc2PzL4dHF9hv'
OIDC_REDIRECT_URI = 'http://localhost:8000/oidc/callback/'
OIDC_STATE_COOKIE_DOMAIN = None

# Your local stuff: Below this line define 3rd party library settings
