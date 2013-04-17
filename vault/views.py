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
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.conf import settings
from django.contrib import messages
from vault.models import CredentialGroup, Credential
from vault.forms import CredentialGroupForm
from utils.encryption import (set_user_encryption_key, clear_user_encryption_key,
    get_user_encryption_key, generate_password)
try:
    import simplejson as json
except ImportError:
    import json

@login_required
def index(request):
    ctx = {}
    try:
        groups = CredentialGroup.objects.filter(Q(owner=request.user) | \
            Q(members__in=[request.user])).order_by('name')
        ctx['credential_groups'] = groups
    except CredentialGroup.DoesNotExist:
        raise Http404()
    return render_to_response('vault/index.html', ctx,
        context_instance=RequestContext(request))

@login_required
def group(request, uuid=None):
    ctx = {}
    try:
        group = CredentialGroup.objects.get(Q(owner=request.user) | \
            Q(members__in=[request.user]), uuid=uuid)
        ctx['group'] = group
    except CredentialGroup.DoesNotExist:
        raise Http404()
    return render_to_response('vault/group.html', ctx,
        context_instance=RequestContext(request))

@login_required
@require_http_methods(["POST"])
def set_key(request):
    nxt = request.GET.get('next', reverse('index'))
    key = request.POST.get('key')
    u = request.user
    set_user_encryption_key(u.username, key)
    return redirect(nxt)

@login_required
def lock_session(request):
    nxt = request.GET.get('next', reverse('index'))
    clear_user_encryption_key(request.user.username)
    return redirect(nxt)

@login_required
def random_password(request):
    return HttpResponse(generate_password())

@login_required
def check_session(request):
    key = get_user_encryption_key(request.user.username)
    if key:
        key = True
    else:
        key = False
    data = {
        'status': key,
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
