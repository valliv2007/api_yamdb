from django.urls import path

from .views import APIToken, SignUp

app_name = 'users'
urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('token/', APIToken.as_view(), name='token'), ]
