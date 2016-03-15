from __future__ import absolute_import
import os
from django.conf import settings
from celery import Celery
from raven import Client
from raven.contrib.celery import register_signal


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    flavor = os.environ.get('FLAVOR')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.{}".format(flavor))

app = Celery('test_app')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if hasattr(settings, 'RAVEN_CONFIG'):
    client = Client(dsn=settings.RAVEN_CONFIG['dsn'])
    register_signal(client)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
