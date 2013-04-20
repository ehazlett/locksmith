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
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from accounts.forms import AccountForm, UserProfileForm
from accounts.models import UserProfile
from datetime import datetime
from utils import billing
import random
import string
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
                messages.error(request, _('Your account is disabled.  Make sure you have activated your account.'))
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
    pform = UserProfileForm(instance=request.user.get_profile())
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user)
        pform = UserProfileForm(request.POST,
            instance=request.user.get_profile())
        if form.is_valid() and pform.is_valid():
            form.save()
            pform.save()
            messages.info(request, _('Account updated.'))
    ctx['form'] = form
    ctx['pform'] = pform
    return render_to_response('accounts/details.html', ctx,
        context_instance=RequestContext(request))

def confirm(request, code=None):
    up = UserProfile.objects.get(activation_code=code)
    user = up.user
    user.is_active = True
    user.save()
    messages.success(request, _('Thanks!  You may now login.'))
    return redirect(reverse('accounts.login'))

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
        username = request.POST.get('username')
        email = request.POST.get('email')
        user = User(first_name=first_name, last_name=last_name,
            email=email)
        user.username = username
        user.set_password(password)
        user.is_active = False
        user.save()
        # generate code
        code = ''.join(random.sample(string.letters+string.digits, 16))
        up = user.get_profile()
        up.activation_code = code
        up.save()
        # send welcome
        tmpl = """Thanks for signing up!

Please activate your account by clicking the following link:

http://{0}{1}

Please feel free to request features, submit bug reports, check the wiki, etc.
at https://github.com/ehazlett/locksmith/wiki

If you have any questions please feel free to contact us at support@vitasso.com.

Thanks!
Locksmith Team
""".format(request.get_host(), reverse('accounts.confirm', args=[code]))
        send_mail(_('Welcome to Locksmith!'), tmpl, settings.ADMIN_EMAIL,
            [user.email], fail_silently=True)
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
