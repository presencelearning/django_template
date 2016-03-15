import uuid
from django.db import models
from django.conf import settings


class HelloWorld(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    hello = models.CharField(max_length=16)

    def __str__(self):
        return str(self.hello)