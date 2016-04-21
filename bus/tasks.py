import logging
logger = logging.getLogger(__name__)

from celery import task
from django.contrib.auth import get_user_model


@task
def auth_user_updated(*args, **kwargs):
    user_uuid = kwargs.get('user_uuid')
    User = get_user_model()
    user, created = User.objects.get_or_create(uuid=user_uuid)
    user.fetch()

    return user
