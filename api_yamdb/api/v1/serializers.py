from datetime import datetime

from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

maxscore = 10
minscore = 1


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

    def validate(self, data):
        """Метод для валидации года"""
        if int(data.get('year') or 0) > datetime.now().year:
            raise serializers.ValidationError(
                'Год не может быть больше текущего')
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для отзывов"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author')

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST':
            title_id = (self.context['view'].kwargs.get('title_id'),)
            author = self.context['request'].user
            if Review.objects.filter(title=title_id, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение.'
                )
        return data

    def validate_score(self, data):
        if maxscore <= data <= minscore:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10'
            )
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
