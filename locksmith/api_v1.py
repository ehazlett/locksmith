from tastypie.resources import ModelResource
from tastypie.authorization import (DjangoAuthorization, Authorization)
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.utils import trailing_slash
from tastypie.bundle import Bundle
from tastypie import fields
from django.core.urlresolvers import reverse
from django.conf.urls.defaults import *
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_user
from django.views.decorators.csrf import csrf_exempt
from vault.models import CredentialGroup, Credential
from tastypie.models import ApiKey
from tastypie.constants import ALL, ALL_WITH_RELATIONS
import simplejson as json
import os

# set csrf exempt to allow mobile login
@csrf_exempt
def api_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username:
        # attempt to parse a json string
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
    user = authenticate(username=username, password=password)
    code = 200
    if user is not None:
        login_user(request, user)
        ur = UserResource()
        user_data = ur.obj_get(request, username=user.username)
        bundle = ur.build_bundle(obj=user_data, request=request)
        data = ur.serialize(None, ur.full_dehydrate(bundle),
            'application/json')
    else:
        data = json.dumps({'error': 'Access denied'})
        code = 403
    return HttpResponse(data, status=code,
        content_type='application/json')

class AppAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        # session based
        if request.user.is_authenticated():
            return True
        else: # check api_key
            if request.META.has_key('HTTP_AUTHORIZATION'):
                auth_header = request.META.get('HTTP_AUTHORIZATION')
                try:
                    username, api_key = auth_header.split()[-1].split(':')
                    # check auth
                    user = User.objects.get(username=username)
                    if user and user.api_key.key == api_key:
                        # auth successful ; set request.user to user for
                        # later user (authorization, filtering, etc.)
                        request.user = user
                        return True
                except:
                    # invalid auth header
                    pass
        return False

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        excludes = ('id', 'password', 'is_staff', 'is_superuser')
        list_allowed_methods = ['get']
        authentication = AppAuthentication()
        authorization = Authorization()
        resource_name = 'accounts'

    # change to prepend_urls for v1.0+
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    # only let non-admin users see their own account
    def apply_authorization_limits(self, request, object_list):
        if not request.user.is_superuser:
            object_list = object_list.filter(username=request.user.username)
        return object_list

    # build custom resource_uri (instead of /resource/<pk>/)
    def get_resource_uri(self, bundle_or_obj):
        kwargs = {
            'resource_name': self._meta.resource_name,
        }
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.username
        else:
            kwargs['pk'] = bundle_or_obj.id

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        return self._build_reverse_url('api_dispatch_detail', kwargs = kwargs)

    def dehydrate(self, bundle):
        # add api_key
        bundle.data['api_key'] = bundle.obj.api_key.key
        return bundle

class CredentialGroupResource(ModelResource):
    class Meta:
        queryset = CredentialGroup.objects.all()
        excludes = ('id', )
        #list_allowed_methods = ['get']
        authentication = AppAuthentication()
        authorization = Authorization()
        resource_name = 'credentialgroups'
        filtering = {
            "name": ALL,
            "description": ALL,
        }

    # change to prepend_urls for v1.0+
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<uuid>[\w\d_.-]+)/$" \
                % self._meta.resource_name, self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
        ]

    def apply_authorization_limits(self, request, object_list):
        if not request.user.is_superuser:
            object_list = object_list.filter(owner=request.user)
        return object_list

    # build custom resource_uri (instead of /resource/<pk>/)
    def get_resource_uri(self, bundle_or_obj):
        kwargs = {
            'resource_name': self._meta.resource_name,
        }
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.uuid
        else:
            kwargs['pk'] = bundle_or_obj.id

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        return self._build_reverse_url('api_dispatch_detail', kwargs = kwargs)

    def obj_create(self, bundle, request, **kwargs):
        # set the owner
        kwargs['owner'] = request.user
        return super(CredentialGroupResource, self).obj_create(bundle, request,
            **kwargs)

class CredentialResource(ModelResource):
    groups = fields.ToManyField(CredentialGroupResource, 'groups', full=True)

    class Meta:
        queryset = Credential.objects.all()
        excludes = ('id', )
        #list_allowed_methods = ['get']
        authentication = AppAuthentication()
        authorization = Authorization()
        resource_name = 'credentials'

    # change to prepend_urls for v1.0+
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<uuid>[\w\d_.-]+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    # build custom resource_uri (instead of /resource/<pk>/)
    def get_resource_uri(self, bundle_or_obj):
        kwargs = {
            'resource_name': self._meta.resource_name,
        }
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.uuid
        else:
            kwargs['pk'] = bundle_or_obj.id

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        return self._build_reverse_url('api_dispatch_detail', kwargs = kwargs)

