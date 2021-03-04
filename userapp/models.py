from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


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
