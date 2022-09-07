# from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Titles, Genre, Category, GenreTitle


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = serializers.SerializerMethodField()
    # rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category')

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            titles = Titles.objects.create(**validated_data)
            return titles
        else:
            genres = validated_data.pop('genre')
            title = Titles.objects.create(**validated_data)
            for genre in genres:
                current_genre, status = (
                    Genre.objects.get_or_create(**genre))
                GenreTitle.objects.create(
                    genre=current_genre, title=title)
            return title

    def get_genre(self, obj):
        return GenreTitle.objects.select_related().filter(title=obj.id)

    # def get_rating(self, obj):
       # return Review.objects.aggregate(Avg('score'))
