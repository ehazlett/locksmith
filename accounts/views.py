from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate, login as login_user,
    logout as logout_user)
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.utils.translation import ugettext as _
from accounts.forms import AccountForm
from accounts.models import UserProfile
from utils import billing

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

def signup(request):
    ctx = {}
    if not settings.SIGNUP_ENABLED:
        messages.warning(request, _('Signup is not enabled at this time.'))
        return redirect(reverse('index'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user = User(first_name=first_name, last_name=last_name,
            email=email)
        user.set_password(password)
        user.save()
        messages.success(request, _('Thanks!  Please check your email to activate.'))
        return redirect(reverse('index'))
    return render_to_response('accounts/signup.html', ctx,
        context_instance=RequestContext(request))

@login_required
def activate(request):
    ctx = {}
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        card_cvc = request.POST.get('card_cvc')
        card_month = request.POST.get('card_month')
        card_year = request.POST.get('card_year')
        card_name = request.POST.get('card_name')
        c = billing.charge(settings.ACCOUNT_COST, card_number=card_number,
            card_exp_month=card_month, card_exp_year=card_year,
            card_cvc=card_cvc, card_name=card_name)
        if c.get('status') == True:
            messages.success(request, _('Thanks for supporting!  Please let us know if you have any questions.'))
            up = request.user.get_profile()
            up.is_pro = True
            up.save()
            return redirect(reverse('index'))
        else:
            messages.error(request, '{0}:{1}'.format(
                _('Error processing payment'), c.get('message')))
            ctx['card_number'] = card_number
            ctx['card_cvc'] = card_cvc
            ctx['card_month'] = card_month
            ctx['card_year'] = card_year
            ctx['card_name'] = card_name
    return render_to_response('accounts/activate.html', ctx,
        context_instance=RequestContext(request))
