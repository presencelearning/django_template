from hello_world.drf.views import HelloWorldViewSet
from plauth.drf.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'helloworld', HelloWorldViewSet)