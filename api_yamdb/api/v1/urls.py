from django.urls import include, path
from rest_framework import routers

from .views import (APIToken, CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUp, TitlesViewSet, UserViewSet)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitlesViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)

urlpatterns_auth = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('token/', APIToken.as_view(), name='token'),
]

urlpatterns = [
    path('v1/auth/', include(urlpatterns_auth)),
    path('v1/', include(router_v1.urls))
]
