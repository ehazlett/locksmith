# Copyright 2013 Evan Hazlett and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as login_user
from django.core.urlresolvers import reverse
from locksmith.api_v1 import UserResource
from social_auth.decorators import dsa_view
import datetime

def index(request):
    ctx = {}
    if request.user.is_authenticated():
        return redirect(reverse('vault.views.index'))
    else:
        return render_to_response('index.html', ctx,
            context_instance=RequestContext(request))

def about(request):
    ctx = {}
    return render_to_response('about.html', ctx,
        context_instance=RequestContext(request))

@dsa_view()
def register_by_access_token(request, backend, *args, **kwargs):
    access_token = request.GET.get('access_token')
    user = backend.do_auth(access_token)
    code = 200
    if user and user.is_active:
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

