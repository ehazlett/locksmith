from django.conf import settings
from django.core.cache import cache
from utils.encryption import get_user_encryption_key

def app_name(request):
    return { 'APP_NAME': getattr(settings, 'APP_NAME')}

def google_analytics_code(request):
    return { 'GOOGLE_ANALYTICS_CODE': getattr(settings, 'GOOGLE_ANALYTICS_CODE')}

def encryption_key(request):
    u = request.user
    key = get_user_encryption_key(u.username)
    return { 'ENCRYPTION_KEY': key }
