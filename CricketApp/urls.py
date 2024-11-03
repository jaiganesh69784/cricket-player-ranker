from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("index.html", views.index, name="index"),
    path("UserLogin.html", views.UserLogin, name="UserLogin"),
    path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
    path("Register.html", views.Register, name="Register"),
    path("Signup", views.Signup, name="Signup"),
    path("Batsman", views.Batsman, name="Batsman"),
    path("Ballers", views.Ballers, name="Ballers"),
]
