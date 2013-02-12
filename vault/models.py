from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

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

class Credential(models.Model):
    uuid = models.CharField(max_length=36, blank=True, null=True,
        default=generate_uuid)
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    key = models.TextField(blank=True, null=True)
    groups = models.ManyToManyField(CredentialGroup, blank=True, null=True)

    def __unicode__(self):
        return '{0}: {1}'.format(self.owner.username, self.name)
