from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("sign-up/", views.signUp, name="sign_Up"),
    path("book/", views.book, name="book"),
    path("pandit/", views.pandit, name="pandit"),
    # path("puja/", views.puja, name="puja"),
    path("puja/<int:id>/", views.puja, name="puja"),
    path("puja/<int:id>/order/", views.order, name="order"),
    path("logout/", views.logout, name="logout"),
]
