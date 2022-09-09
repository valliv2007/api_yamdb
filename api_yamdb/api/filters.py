import django_filters

from reviews.models import Titles


class TitlesFilter(django_filters.FilterSet):
    """Фильтр для произведений"""

    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains",)
    year = django_filters.NumberFilter(field_name="year")
    category = django_filters.CharFilter(
        field_name="category__slug")
    genre = django_filters.CharFilter(
        field_name="genre__slug")

    class Meta:
        model = Titles
        fields = ['name', 'year', 'category', 'genre']
