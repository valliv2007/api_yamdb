from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from .models import FORBIDDEN_USERNAME, ROLES, User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    role = serializers.ChoiceField(choices=ROLES, required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate(self, data):
        if data['username'] == FORBIDDEN_USERNAME:
            raise serializers.ValidationError(
                f'{FORBIDDEN_USERNAME} недопустимое имя пользователя')
        return data


class JWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise exceptions.NotFound(
                'Такого пользователя не существует')
        return data
