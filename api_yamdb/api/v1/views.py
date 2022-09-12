from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Category, Genre, Review, Title
from .filters import TitlesFilter
from .mixins import GetPostDeleteViewSet
from .permissions import AdminOrReadOnly, ReviewAndComment
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitlesPostDeleteSerializer, TitlesReadSerializer)


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений"""

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score'),
    ).order_by('id')
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        """Определение сериалайзера для произведений"""
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesPostDeleteSerializer


class CategoryViewSet(GetPostDeleteViewSet):
    """Вьюсет для категорий"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(GetPostDeleteViewSet):
    """Вьюсет для жанров"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обзоров"""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, ReviewAndComment)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев"""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, ReviewAndComment)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
