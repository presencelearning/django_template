from hello_world.drf.serializers import HelloWorldSerializer
from hello_world.models import HelloWorld
from rest_framework import viewsets


class HelloWorldViewSet(viewsets.ModelViewSet):
    queryset = HelloWorld.objects.all()
    serializer_class = HelloWorldSerializer
    lookup_field = 'uuid'
    lookup_value_regex = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'