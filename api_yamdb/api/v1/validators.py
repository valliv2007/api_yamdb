from rest_framework import serializers

from users.models import FORBIDDEN_USERNAME


def validate_user(data):
    """Вальдатор на использование запрещённого имени"""
    if data.get('username') == FORBIDDEN_USERNAME:
        raise serializers.ValidationError(
            f'{FORBIDDEN_USERNAME} недопустимое имя пользователя')
