from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.cache import cache
from uuid import uuid4
from utils.encryption import encrypt, get_user_encryption_key
from locksmith.middleware import threadlocal

def generate_uuid():
    return str(uuid4())

class CredentialGroup(models.Model):
    uuid = models.CharField(max_length=36, blank=True, null=True,
        default=generate_uuid)
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, blank=True, null=True,
        related_name='credential_group_owner')
    members = models.ManyToManyField(User, blank=True, null=True,
        related_name='credential_group_members')

    def __unicode__(self):
        return '{0}: {1}'.format(self.owner.username, self.name)

    def get_credentials(self):
        return Credential.objects.filter(groups__in=[self])

class Credential(models.Model):
    uuid = models.CharField(max_length=36, blank=True, null=True,
        default=generate_uuid)
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    username = models.CharField(max_length=96, blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    groups = models.ManyToManyField(CredentialGroup, blank=True, null=True)

    def __unicode__(self):
        return '{0}: {1}'.format(','.join([x.name for x in self.groups.all()]),
            self.name)

    def save(self, *args, **kwargs):
        user = threadlocal.get_current_user()
        key = get_user_encryption_key(user.username) or kwargs.get('key')
        # if no key throw error
        if not key:
            raise StandardError("If calling save from outside of a request, " \
                "you must specify 'key' as a kwarg")
        self.password = encrypt(self.password, key)
        super(Credential, self).save(*args, **kwargs)
