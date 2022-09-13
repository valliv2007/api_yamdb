import logging
import os.path
from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
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

logging.getLogger().setLevel(logging.INFO)


class Command(BaseCommand):
    """ Команда для загрузки данных в БД"""

    def handle(self, *args, **options):
        for row in DictReader(open(DATA_PATCH['users'], encoding='utf-8')):
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

        logging.info('База user загружена')

        for row in DictReader(open(DATA_PATCH['category'], encoding='utf-8')):
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            category.save()

        logging.info('База category загружена')

        for row in DictReader(open(DATA_PATCH['genre'], encoding='utf-8')):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            genre.save()

        logging.info('База genre загружена')

        for row in DictReader(open(DATA_PATCH['titles'], encoding='utf-8')):
            title = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category'],
            )
            title.save()

        logging.info('База title загружена')

        for row in DictReader(
                open(DATA_PATCH['genre_title'], encoding='utf-8')):
            genre_title = GenreTitle(
                id=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id'],
            )
            genre_title.save()

        logging.info('База genre_title загружена')

        for row in DictReader(open(DATA_PATCH['review'], encoding='utf-8')):
            review = Review(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date'],
            )
            review.save()

        logging.info('База review загружена')

        for row in DictReader(open(DATA_PATCH['comments'], encoding='utf-8')):
            comments = Comment(
                id=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date'],
            )
            comments.save()

        logging.info('База comments загружена')
