from django.conf import settings
import os

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    flavor = os.environ.get('FLAVOR', 'dev')
    settings_module = "config.settings.{flavor}".format(flavor=flavor)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

from pl.bus import worker

app = worker.app