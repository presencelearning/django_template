from django.db import models
from django.contrib.auth.models import PermissionsMixin


class UserManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class User(PermissionsMixin):
    USERNAME_FIELD = 'uuid'
    REQUIRED_FIELDS = []
    uuid = models.UUIDField(unique=True)

    last_login = models.DateTimeField('last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.')

    objects = UserManager()

    def __str__(self):
        return str(self.uuid)

    def get_full_name(self):
        return str(self.uuid)

    def get_short_name(self):
        return str(self.uuid)

    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True