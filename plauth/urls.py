from django.conf.urls import url
from pl.user import views

urlpatterns = [
    url(r'^login/$', views.oidc_login, name='oidc_login'),
    url(r'^callback/$', views.oidc_callback, name='oidc_callback'),
]