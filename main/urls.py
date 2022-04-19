from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("sign-up/", views.signUp, name="sign_Up"),
    path("book/", views.book, name="book"),
    path("puja/", views.puja, name="puja"),
    path("order/", views.order, name="order"),
    path("logout/", views.logout, name="logout"),
]
