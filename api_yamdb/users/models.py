from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (('user', 'Аутентифицированный пользователь'),
         ('moderator', 'Модератор'),
         ('admin', 'Администратор'))


class User (AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя', max_length=15, choices=ROLES, default='user')
