from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime
from utils.encryption import decrypt

register = template.Library()

@register.filter(takes_context=True)
@stringfilter
def decrypt(context, data=None):
    request = context['request']
    key = request.session.get('key')
    return decrypt(data, key)

@register.filter
def timestamp(value):
    try:
        return datetime.fromtimestamp(value)
    except AttributeError:
        return ''
