from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Puja, Order

# Create your views here.


def home(response):
    return render(response, "homepage.html", {})


def login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, "User logged in successfully")
            print("User logged in successfully")
            return redirect("../")
        else:
            print("invalid credentials")
            messages.info(request, "Invalid credatials")
            return redirect("/login")
    return render(request, "login.html", {})


def signUp(request):
    if request.method == 'POST':
        username = request.POST['uname']
        email = request.POST['email']
        password1 = request.POST['pass']
        password2 = request.POST['pass2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print("Username already exists")
                messages.info(request, 'Username already exists')
                return redirect("/sign-up")
            elif User.objects.filter(email=email).exists():
                print("Email already exists")
                messages.info(request, 'Email already exists')
                return redirect("/sign-up")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1)
                user.save()
                print("user created")
        else:
            print("check passwords not matching")
            messages.info(request, 'Password not matching')
            return redirect("/")
        return redirect("../login/")

    else:
        return render(request, "signup.html", {})


def book(response):
    return render(response, "book.html", {})


def puja(response):
    return render(response, "MahalaxmifullInfo.html", {})


@login_required
def order(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['optradio']
        password2 = request.POST['pass2']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        address = address1 + ' ' + address2 + ' ' + city + ' ' + state + ' ' + zip

        #pujaName = models.ForeignKey(Puja, on_delete=models.CASCADE)
        #mobile_no = models.CharField(max_length=15)
        # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        # phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
        #dateOfPuja = models.DateTimeField()
        #total_pay = models.CharField(max_length=50)
        myOrder = Order.objects.create(
            first_name=first_name, last_name=last_name, address=address, )
        return render(request, '../')
    else:
        return render(request, "order.html", {})


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")
