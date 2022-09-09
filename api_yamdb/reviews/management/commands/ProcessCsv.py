import os
from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import (Category, Titles, Genre, GenreTitle, Review,
                            Comment)
from users.models import User


DATA_DIR = 'static/data'
DATA_PATCH = {
    'users': os.path.join(DATA_DIR, 'users.csv'),
    'category': os.path.join(DATA_DIR, 'category.csv'),
    'genre': os.path.join(DATA_DIR, 'genre.csv'),
    'titles': os.path.join(DATA_DIR, 'titles.csv'),
    'genre_title': os.path.join(DATA_DIR, 'genre_title.csv'),
    'review': os.path.join(DATA_DIR, 'review.csv'),
    'comments': os.path.join(DATA_DIR, 'comments.csv'),
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for row in DictReader(open(DATA_PATCH['users'])):
            user = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            user.save()

        print('Данные user загружены')

        for row in DictReader(open(DATA_PATCH['category'])):
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            category.save()

        print('Данные category загружены')

        for row in DictReader(open(DATA_PATCH['genre'])):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            genre.save()

        print('Данные genre загружены')

        for row in DictReader(open(DATA_PATCH['titles'])):
            title = Titles(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category'],
            )
            title.save()

        print('Данные title загружены')

        for row in DictReader(open(DATA_PATCH['genre_title'])):
            genre_title = GenreTitle(
                id=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id'],
            )
            genre_title.save()

        print('Данные genre_title загружены')

        for row in DictReader(open(DATA_PATCH['review'])):
            review = Review(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date'],
            )
            review.save()

        print('Данные review загружены')

        for row in DictReader(open(DATA_PATCH['comments'])):
            comments = Comment(
                id=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date'],
            )
            comments.save()

        print('Данные comments загружены')
