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

def stripe_info(request):
    return {
        'STRIPE_API_KEY': getattr(settings, 'STRIPE_API_KEY'),
        'STRIPE_PUBLISHABLE_KEY': getattr(settings, 'STRIPE_PUBLISHABLE_KEY'),
    }

def intercom_app_id(request):
    return { 'INTERCOM_APP_ID': getattr(settings, 'INTERCOM_APP_ID')}

def encryption_key(request):
    u = request.user
    key = get_user_encryption_key(u.username)
    return { 'ENCRYPTION_KEY': key }

def signup_enabled(request):
    return { 'SIGNUP_ENABLED': getattr(settings, 'SIGNUP_ENABLED')}
