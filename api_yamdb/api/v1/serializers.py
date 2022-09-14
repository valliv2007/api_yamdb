from django.utils import timezone
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.constants import MAX_SCORE, MIN_SCORE, MESSAGE_ERR_SCORE, ROLES
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from .validators import validate_user


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для категорий"""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для жанров"""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesReadSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения произведений"""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True, allow_null=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class TitlesPostDeleteSerializer(serializers.ModelSerializer):
    """Сериалайзер для публикации и удаления произведений"""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    genre = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(), slug_field='slug')
    rating = serializers.FloatField(read_only=True, allow_null=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def validate_year(self, data):
        """Метод для валидации года"""
        if data > timezone.now().year:
            raise serializers.ValidationError(
                'Год не может быть больше текущего')
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для отзывов"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id',)

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            author = self.context['request'].user
            if Review.objects.filter(
                    title__id=title_id, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение.'
                )
        return data

    def validate_score(self, data):
        if MAX_SCORE < data < MIN_SCORE:
            raise serializers.ValidationError(MESSAGE_ERR_SCORE)
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для комментариев к отзывам"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id',)


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для пользователей"""
    email = serializers.EmailField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)

    def validate_username(self, data):
        validate_user(data)
        if not data:
            raise serializers.ValidationError('Отстутвие обязательного поля')
        return data

    def validate_email(self, data):
        if not data:
            raise serializers.ValidationError('Отстутвие обязательного поля')
        return data


class AdminSerializer(serializers.ModelSerializer):
    """Сериалайзер для админа"""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    role = serializers.ChoiceField(choices=ROLES, required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate(self, data):
        validate_user(data)
        return data


class JWTTokenSerializer(serializers.Serializer):
    """Сериалайзер для получения токена"""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise exceptions.NotFound(
                'Такого пользователя не существует')
        return data
