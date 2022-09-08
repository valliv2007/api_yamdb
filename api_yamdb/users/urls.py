from django.urls import path

from .views import APIToken, SignUp

urlpatterns = [
    path('signup/', SignUp.as_view()),
    path('token/', APIToken.as_view()), ]