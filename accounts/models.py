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
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from tastypie.models import create_api_key

class UserProfile(models.Model):
    """
    User profile

    """
    user = models.ForeignKey(User, unique=True)
    encryption_key_timeout = models.IntegerField(default=3600, blank=True,
        null=True)
    is_pro = models.NullBooleanField(default=False, null=True, blank=True)
    pro_join_date = models.DateTimeField(null=True, blank=True)
    customer_id = models.CharField(max_length=64, null=True, blank=True)
    activation_code = models.CharField(max_length=64, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

# create user profile upon save
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_api_key, sender=User)

