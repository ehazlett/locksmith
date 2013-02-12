from django.conf import settings

def app_name(context):
    return { 'APP_NAME': getattr(settings, 'APP_NAME')}

def google_analytics_code(context):
    return { 'GOOGLE_ANALYTICS_CODE': getattr(settings, 'GOOGLE_ANALYTICS_CODE')}
