from ..models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('id', 'uuid', 'created', 'modified', 'is_staff', 'is_superuser')
        extra_kwargs = {
            'url': {'view_name': 'user-detail', 'lookup_field': 'uuid'}
        }