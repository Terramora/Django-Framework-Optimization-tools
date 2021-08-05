import pytz
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.conf import settings


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_image', blank=True)

    active_key = models.CharField(max_length=128, blank=True)
    active_key_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def active_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) < self.active_key_created + timedelta(hours=2):
            return False
        else:
            return True


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, db_index=True)
    tagline = models.CharField(max_length=150, blank=True, verbose_name='Теги')
    about = models.TextField(blank=True, verbose_name='О себе')
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, max_length=1, verbose_name='гендер')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        instance.userprofile.save()