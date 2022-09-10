from api.permissions import IsAdmin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .models import User
from .serializers import AdminSerializer, JWTTokenSerializer, UserSerializer


def send_confirmation_code_on_email(username, email):
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(subject='Confirmation code for YaMDb',
              message=f'Ваш код {confirmation_code}',
              from_email=DEFAULT_FROM_EMAIL,
              recipient_list=[email])


class SignUp(APIView):
    """Вьюкласс для регистрации пользователей"""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if User.objects.filter(
                username=serializer.initial_data.get('username'),
                email=serializer.initial_data.get('email')).exists():
            send_confirmation_code_on_email(
                serializer.initial_data['username'],
                serializer.initial_data['email'])
            return Response(serializer.initial_data, status=status.HTTP_200_OK)
        if serializer.is_valid():
            serializer.save()
            send_confirmation_code_on_email(
                serializer.data['username'], serializer.data['email'])
            return Response(serializer.initial_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIToken(APIView):
    """Вьюкласс для получения токена"""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = JWTTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User, username=serializer.data['username'])
            if default_token_generator.check_token(user,
                                                   serializer.data[
                                                       'confirmation_code']):
                token = AccessToken.for_user(user)
                return Response(
                    {'token': str(token)}, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы админа с пользователями"""

    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'


class UserView(APIView):
    """Вьюкласс для просмотра и изменения данных своей учетной записи"""

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(
            user, data=request.data, partial=True, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
