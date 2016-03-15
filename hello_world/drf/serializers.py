from hello_world.models import HelloWorld
from rest_framework import serializers


class HelloWorldSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail',
        lookup_field='uuid'
    )

    class Meta:
        model = HelloWorld
        read_only_fields = ('id', 'uuid', 'created', 'modified',)
        extra_kwargs = {
            'url': {'view_name': 'helloworld-detail', 'lookup_field': 'uuid'}
        }
