from django.db import models
from tastypie.models import create_api_key
from django.contrib.auth.models import User

# create user profile upon save
models.signals.post_save.connect(create_api_key, sender=User)

