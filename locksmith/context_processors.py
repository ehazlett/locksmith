from django.conf import settings
from django.core.cache import cache

def app_name(request):
    return { 'APP_NAME': getattr(settings, 'APP_NAME')}

def google_analytics_code(request):
    return { 'GOOGLE_ANALYTICS_CODE': getattr(settings, 'GOOGLE_ANALYTICS_CODE')}

def encryption_key(request):
    u = request.user
    key = cache.get(settings.CACHE_ENCRYPTION_KEY.format(u.username))
    return { 'ENCRYPTION_KEY': key }
