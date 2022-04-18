from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(response):
    return render(response, "main/homepage.html", {})

def book(response):
    return render(response, "main/book.html", {})

def puja(response):
    return render(response, "main/MahalaxmifullInfo.html", {})

def order(response):
    return render(response, "main/order.html", {})


