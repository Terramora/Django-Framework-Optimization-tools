import pytz
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.conf import settings


# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_image', blank=True)

    active_key = models.CharField(max_length=128, blank=True)
    active_key_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def active_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) < self.active_key_created + timedelta(hours=2):
            return False
        else:
            return True
