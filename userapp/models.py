from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(verbose_name='Аватарка пользователя', upload_to='users_avatars', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='Возраст пользователя', blank=True, null=True)
