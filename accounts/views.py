from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate, login as login_user,
    logout as logout_user)
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from accounts.forms import AccountForm
from accounts.models import UserProfile
from datetime import datetime
from utils import billing
try:
    import simplejson as json
except ImportError:
    import json

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
        token = request.POST.get('token')
        try:
            customer = billing.create_customer(token, settings.ACCOUNT_PLAN,
                request.user.email)
            up = request.user.get_profile()
            up.customer_id = customer.id
            up.save()
            messages.success(request, _('Thanks for supporting!  Please let us know if you have any questions.'))
            return redirect(reverse('index'))
        except Exception, e:
            messages.error(request, '{0}:{1}'.format(
                _('Error processing payment'), e))
    return render_to_response('accounts/activate.html', ctx,
        context_instance=RequestContext(request))

@csrf_exempt
def hook(request):
    event = json.loads(request.body)
    print(event)
    event_type = event.get('type')
    # subscription payment success
    if event_type == 'invoice.payment_succeeded':
        customer = event.get('data', {}).get('object', {}).get('customer')
        up = UserProfile.objects.get(customer_id=customer)
        if settings.DEBUG or event.get('livemode'):
            up.is_pro = True
            up.pro_join_date = datetime.now()
            up.save()
    # subscription ended
    if event_type == 'customer.subscription.deleted' or \
        event_type == 'charge.refunded' or event_type == 'charge.failed' or \
        event_type == 'customer.subscription.deleted' or \
        event_type == 'invoice.payment_failed':
        customer = event.get('data', {}).get('object', {}).get('customer')
        up = UserProfile.objects.get(customer_id=customer)
        if settings.DEBUG or event.get('livemode'):
            up.is_pro = False
            up.save()
    return HttpResponse(status=200)
