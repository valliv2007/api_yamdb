from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

ROLES = (('user', 'Аутентифицированный пользователь'),
         ('moderator', 'Модератор'),
         ('admin', 'Администратор'))
FORBIDDEN_USERNAME = 'me'


class APIUserManager(UserManager):
    """Модель управления созданием пользователей"""

    def create_user(self, username, **extra_fields):
        if username == FORBIDDEN_USERNAME:
            raise ValueError(
                f'{FORBIDDEN_USERNAME} недопустимое имя пользователя')
        return super().create_user(username, **extra_fields)

    def create_superuser(self, username, role='admin', **extra_fields):
        return super().create_superuser(username, role='admin', **extra_fields)


class User (AbstractUser):
    """Модель прользователей"""

    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя', max_length=15, choices=ROLES, default='user')
    email = models.EmailField('E-mail', unique=True, blank=False)
    objects = APIUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
