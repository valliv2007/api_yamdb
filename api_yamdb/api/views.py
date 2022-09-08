from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny

from .mixins import GetPostDeleteViewSet
from reviews.models import Titles, Genre, Category
from .serializers import CategorySerializer, GenreSerializer
from .serializers import TitlesReadSerializer, TitlesPostDeleteSerializer
from .permissions import AdminOrReadOnly


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'year', 'category', 'genre')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesPostDeleteSerializer


class CategoryViewSet(GetPostDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
