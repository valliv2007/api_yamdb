from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from reviews.models import Category, Genre, Titles
from .filters import TitlesFilter
from .mixins import GetPostDeleteViewSet
from .permissions import AdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitlesPostDeleteSerializer, TitlesReadSerializer)


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений"""

    queryset = Titles.objects.all()
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
