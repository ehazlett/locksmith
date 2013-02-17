# coding: utf-8
# Copied from https://github.com/jedie/django-tools/blob/master/django_tools/middlewares/ThreadLocal.py
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

def get_current_request():
    """ returns the request object for this thead """
    return getattr(_thread_locals, "request", None)

def get_current_user():
    """ returns the current user, if exist, otherwise returns None """
    request = get_current_request()
    if request:
        return getattr(request, "user", None)

def get_current_session():
    """ returns the current user, if exist, otherwise returns None """
    request = get_current_request()
    if request:
        return getattr(request, "session", None)

class ThreadLocalMiddleware(object):
    """ Simple middleware that adds the request object in thread local storage."""
    def process_request(self, request):
        _thread_locals.request = request
