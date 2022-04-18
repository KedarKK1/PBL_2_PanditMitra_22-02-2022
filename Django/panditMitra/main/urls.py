from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("book/", views.book, name="book"),
    path("puja/", views.puja, name="puja"),
    path("order/", views.order, name="order"),

]
