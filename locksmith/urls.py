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
    url(r'^accounts/', include('accounts.urls')),
    url(r'^vault/', include('vault.urls')),
    url(r'', include('social_auth.urls')),
)

# to serve media in cloudfoundry
if os.environ.has_key('VCAP_SERVICES') or settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATICFILES_DIRS[0],
        }),
    )
