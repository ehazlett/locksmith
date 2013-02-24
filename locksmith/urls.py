import os
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from locksmith.api_v1 import (UserResource, CredentialGroupResource,
    CredentialResource)

admin.autodiscover()

# api
api_v1 = Api(api_name='v1')
api_v1.register(UserResource())
api_v1.register(CredentialGroupResource())
api_v1.register(CredentialResource())

urlpatterns = patterns('',
    url(r'^$', 'locksmith.views.index', name='index'),
    url(r'^about/$', 'locksmith.views.about', name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_v1.urls)),
    url(r'^api/login', 'locksmith.api_v1.api_login'),
    url(r'^auth/(?P<backend>[^/]+)/$',
        'locksmith.views.register_by_access_token'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^vault/', include('vault.urls')),
    url(r'', include('social_auth.urls')),
)
