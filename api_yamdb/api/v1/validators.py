from rest_framework import serializers

from api_yamdb.constants import FORBIDDEN_USERNAME


def validate_user(data):
    """Вальдатор на использование запрещённого имени"""
    if data == FORBIDDEN_USERNAME:
        raise serializers.ValidationError(
            f'{FORBIDDEN_USERNAME} недопустимое имя пользователя')
