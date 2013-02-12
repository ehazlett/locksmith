from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from social_auth.decorators import dsa_view
import datetime

def index(request):
    ctx = {}
    return render_to_response('index.html', ctx,
        context_instance=RequestContext(request))

def about(request):
    ctx = {}
    return render_to_response('about.html', ctx,
        context_instance=RequestContext(request))

@dsa_view()
def register_by_token(request, backend, *args, **kwargs):
    access_token = request.GET.get('access_token')
    user = backend.do_auth(access_token)
    if user and user.is_active():
        login_user(request, user)
    return redirect(reverse('index'))

