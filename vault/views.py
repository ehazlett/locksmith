from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib import messages
from vault.models import CredentialGroup, Credential
from vault.forms import CredentialGroupForm

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
    key = request.POST.get('key')
    request.session['key'] = key
    return redirect(reverse('index'))
