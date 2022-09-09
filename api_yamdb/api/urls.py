from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet, TitlesViewSet
from users.views import AdminViewSet, UserViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'v1/titles', TitlesViewSet)
router_v1.register(r'v1/categories', CategoryViewSet)
router_v1.register(r'v1/genres', GenreViewSet)
router_v1.register(r'v1/users/me', UserViewSet, basename='users_me')
router_v1.register(r'v1/users', AdminViewSet)
urlpatterns = [
    path('', include(router_v1.urls))
]
