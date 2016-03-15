# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hello_world.urls
import hello_world.views

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.defaults import bad_request, permission_denied, page_not_found, server_error
from .api_urls import router

urlpatterns = [
    # Django Admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^oidc/', include('plauth.urls')),
    # Your stuff: custom urls includes go here
    url(r'^api/v1/', include(router.urls)),
    # example
    url(r'^helloworld/', include(hello_world.urls)),
    url(r'^$', hello_world.views.index)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', bad_request),
        url(r'^403/$', permission_denied),
        url(r'^404/$', page_not_found),
        url(r'^500/$', server_error),
    ]
