from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from api_yamdb.constants import (ADMIN, FORBIDDEN_USERNAME,
                                 MODERATOR, ROLES, USER)


class APIUserManager(UserManager):
    """Модель управления созданием пользователей"""

    def create_user(self, username, **extra_fields):
        if username == FORBIDDEN_USERNAME:
            raise ValueError(
                f'{FORBIDDEN_USERNAME} недопустимое имя пользователя')
        return super().create_user(username, **extra_fields)

    def create_superuser(self, username, role=ADMIN, **extra_fields):
        return super().create_superuser(
            username, role=ADMIN, **extra_fields)


class User (AbstractUser):
    """Модель прользователей"""

    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя', max_length=15, choices=ROLES, default=USER)
    email = models.EmailField('E-mail', unique=True, blank=False)
    objects = APIUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR
