from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate, login as login_user,
    logout as logout_user)
from django.contrib import messages
from django.utils.translation import ugettext as _
from accounts.forms import AccountForm

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login_user(request, user)
                return redirect(reverse('index'))
            else:
                messages.error(request, _('Your account is disabled.  Please contact support.'))
        else:
            messages.error(request, _('Invalid username/password'))
    return render_to_response('accounts/login.html',
        context_instance=RequestContext(request))

def logout(request):
    logout_user(request)
    return redirect(reverse('index'))

@login_required
def details(request):
    ctx = {}
    form = AccountForm(instance=request.user)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, _('Account updated.'))
    ctx['form'] = form
    return render_to_response('accounts/details.html', ctx,
        context_instance=RequestContext(request))

