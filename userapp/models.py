from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    avatar = models.ImageField(verbose_name='Аватарка пользователя', upload_to='users_avatars', blank=True)
    age = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    activation_key = models.CharField(verbose_name='Код активации пользователя', max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(verbose_name='Время жизни ключа', default=(now() + timedelta(hours=24)))

    def check_activation_key(self):
        if now() < self.activation_key_expires:
            return True
        else:
            return False


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICE = (
        (MALE, 'М'),
        (FEMALE, 'Ж')
    )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='Тэги пользователя', max_length=128, blank=True)
    about = models.TextField(verbose_name='Описание пользователя о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='Пол пользователя', max_length=1, choices=GENDER_CHOICE, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
