from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import JWTTokenSerializer, UserSerializer


def send_confirmation_code_on_email(username, email):
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(subject='Код подтверждения для регистриции на YaMDb',
              message=f'Ваш код {confirmation_code}',
              recipient_list=[email])


class SignUp(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer
        if serializer.is_valid():
            serializer.save()
            send_confirmation_code_on_email(
                serializer.data['username'], serializer.data['email'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = JWTTokenSerializer
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
