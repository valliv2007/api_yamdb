from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitlesFilter
from .mixins import GetPostDeleteViewSet
from .permissions import AdminOrReadOnly, IsAdmin, ReviewAndComment
from .serializers import (AdminSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          JWTTokenSerializer, ReviewSerializer,
                          TitlesPostDeleteSerializer, TitlesReadSerializer,
                          UserSerializer)


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений"""

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('id')
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


def send_confirmation_code_on_email(username, email):
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(subject='Confirmation code for YaMDb',
              message=f'Ваш код {confirmation_code}',
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[email])


class SignUp(APIView):
    """Вьюкласс для регистрации пользователей"""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            User.objects.get_or_create(
                username=serializer.data.get('username'),
                email=serializer.data.get('email'))
        except IntegrityError as error:
            return Response(
                {'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        send_confirmation_code_on_email(
            serializer.data['username'], serializer.data['email'])
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIToken(APIView):
    """Вьюкласс для получения токена"""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = JWTTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.data['username'])
        if default_token_generator.check_token(
           user, serializer.data['confirmation_code']):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'confirmation_code': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы админа с пользователями"""

    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=('get', 'patch'),
            url_name='me', permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True, many=False)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
