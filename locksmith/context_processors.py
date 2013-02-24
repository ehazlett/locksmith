from django.conf import settings
from django.core.cache import cache
from utils.encryption import get_user_encryption_key

def app_info(request):
    return {
        'APP_NAME': getattr(settings, 'APP_NAME'),
        'APP_REVISION': getattr(settings, 'APP_REVISION'),
    }

def google_analytics_code(request):
    return { 'GOOGLE_ANALYTICS_CODE': getattr(settings, 'GOOGLE_ANALYTICS_CODE')}

def intercom_app_id(request):
    return { 'INTERCOM_APP_ID': getattr(settings, 'INTERCOM_APP_ID')}

def encryption_key(request):
    u = request.user
    key = get_user_encryption_key(u.username)
    return { 'ENCRYPTION_KEY': key }

def signup_enabled(request):
    return { 'SIGNUP_ENABLED': getattr(settings, 'SIGNUP_ENABLED')}
