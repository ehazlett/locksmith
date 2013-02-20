from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.conf import settings
from django.contrib import messages
from vault.models import CredentialGroup, Credential
from vault.forms import CredentialGroupForm
from utils.encryption import (set_user_encryption_key, clear_user_encryption_key,
    generate_password)

@login_required
def index(request):
    ctx = {}
    ctx['credential_groups'] = CredentialGroup.objects.filter(
        owner=request.user).order_by('name')
    return render_to_response('vault/index.html', ctx,
        context_instance=RequestContext(request))

@login_required
def group(request, uuid=None):
    ctx = {}
    group = CredentialGroup.objects.get(uuid=uuid)
    ctx['group'] = group
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

