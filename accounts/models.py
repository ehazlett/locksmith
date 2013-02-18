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

    def __unicode__(self):
        return self.user.username

# create user profile upon save
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_api_key, sender=User)

