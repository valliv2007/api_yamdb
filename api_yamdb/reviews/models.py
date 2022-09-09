from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Genre(models.Model):
    """Модель жанров"""
    name = models.CharField(verbose_name='Жанр', max_length=256)
    slug = models.SlugField(verbose_name='Адрес страницы жанра', unique=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категорий для произведений"""

    name = models.CharField(verbose_name='Категория', max_length=256)
    slug = models.SlugField(
        verbose_name='Адрес страницы категории',
        unique=True,
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Titles(models.Model):
    """Модель произведений"""

    name = models.CharField(verbose_name='Произведение', max_length=256)
    year = models.IntegerField(verbose_name='Год',)
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель взаимосвязи жанров и произведений"""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Genre title'
        verbose_name_plural = 'Genres titles'

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """Отзыв на произведение"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Описание",
    )
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique review"
            )
        ]

        verbose_name = "Review"
        verbose_name_plural = 'Reviews'


class Comment(models.Model):
    """Комментарий к отзыву произведения"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = 'Comments'