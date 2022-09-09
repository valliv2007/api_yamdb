from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Titles, Genre, Category, Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def get_rating(self, obj):
        score = Review.objects.filter(title_id=obj.id).aggregate(Avg('score'))

        return score['score__avg']


class TitlesPostDeleteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    genre = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(), slug_field='slug')
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def get_rating(self, obj):
        score = Review.objects.filter(title_id=obj.id).aggregate(Avg('score'))

        return score['score__avg']

    def validate(self, data):
        if data['year'] > datetime.now().year:
            raise serializers.ValidationError(
                'Год не может быть больше текущего')

        return data
