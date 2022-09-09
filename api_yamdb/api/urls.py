from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet, TitlesViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'v1/titles', TitlesViewSet)
router_v1.register(r'v1/categories', CategoryViewSet)
router_v1.register(r'v1/genres', GenreViewSet)

urlpatterns = [
    path('', include(router_v1.urls))
]
