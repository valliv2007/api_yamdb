from django.urls import path

from .views import APIToken, SignUp

app_name = 'users'
urlpatterns = [
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/auth/token/', APIToken.as_view(), name='token'), ]
