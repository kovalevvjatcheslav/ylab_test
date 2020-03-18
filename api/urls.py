from django.urls import path
from .views import SignUp, SignIn, Transfer

urlpatterns = [
    path('signup/', SignUp.as_view()),
    path('signin/', SignIn.as_view()),
    path('transfer/', Transfer.as_view()),
]
