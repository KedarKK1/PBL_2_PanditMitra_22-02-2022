from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from pyrsistent import v
from .models import *
import datetime
from django.core.mail import send_mail
from django.db import connections
import sqlite3
import os
import os.path
from django.db.models import Avg, Count, FloatField
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import datetime
import random

# Create your views here.


def handler404(request, exception):
    return render(request, "errorPage.html", {})


def handler403(request):
    return render(request, "errorPage.html", {})


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
            # print("User logged in successfully")
            return redirect("../")
        else:
            # print("invalid credentials")
            messages.info(request, "Invalid credatials")
            return redirect("/login")
    return render(request, "login.html", {})


def confirmation(request, id):
    if(request.method == 'POST'):
        mySecreteKey = request.POST['mySecreteKey']
        mySecreteKey = int(mySecreteKey)
        # print("mySecreteKey is ", mySecreteKey," and it type is ", type(mySecreteKey))
        myUser1 = myUser.objects.get(id=id)
        # print("myUser found ", myUser1)
        userSecretKey = myUser1.secretKey
        # print("User secret key is ", userSecretKey," and its type is ", type(userSecretKey))
        if(mySecreteKey == userSecretKey):
            username = myUser1.username
            password1 = myUser1.password
            print("password of user was", password1)
            email = myUser1.email
            user = User.objects.create_user(
                username=username, email=email, password=password1)
            user.save()
            # print("user created")
            messages.info(request, "User created successfully!! Please login")
            return redirect('login')
        else:
            print("check OTP not matching")
            messages.info(request, 'OTP not matching')
            return redirect(request.path)
    return render(request, "confirmation.html", {})


def signUp(request):
    if request.method == 'POST':
        username = request.POST['uname']
        email = request.POST['email']
        password1 = request.POST['pass']
        password2 = request.POST['pass2']
        myRandomKey = random.randint(100000, 999999)
        print("random key generated equal to ", myRandomKey)
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
                # send email
                template = render_to_string(
                    'signUpEmail.html', {'username': username, 'myRandomKey': myRandomKey})
                # email1 = EmailMessage(
                #     'Sign Up link for PanditMitra',  # subject
                #     template,  # message
                #     settings.EMAIL_HOST_USER,  # from Email
                #     [email],  # to email
                # )
                # email1.fail_silently=False
                # email1.send()

                try:
                    send_mail('Verification link for PanditMitra',
                              template, settings.EMAIL_HOST_USER, [email])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                myUser1 = myUser.objects.create(
                    username=username, email=email, password=password1, secretKey=myRandomKey)
                myUser1id = myUser1.id
                # print('myUser created')
                return redirect('confirmation', id=myUser1id)

        else:
            # print("check passwords not matching")
            messages.info(request, 'Password not matching')
            return redirect(request.path)
        # return redirect('login')

    else:
        return render(request, "signup.html", {})

# def panditLogin(request):
    # return render(request, "panditLogin.html", {})


def sortBook(request, nameOfPuja):
    ls = Puja.objects.filter(nameOfPuja=nameOfPuja)
    print(ls)
    return render(request, "book.html", {})


def reviews(response):
    return render(response, "chooseReview.html", {})


def choosePujaForReview(response):
    myPujas = Puja.objects.all()
    # print(myPujas)
    return render(response, "choosePujaForReview.html", {"ls": myPujas})


def seeReviews(response):
    ls = Reviews.objects.all()
    myPujas = Puja.objects.all()
    # ls2 = str(Reviews.objects.values_list('created_date'))
    # print(ls2)
    # above code for objects.values_list is working

    ls2 = Reviews.objects.values_list('created_date')
    # data = datetime.datetime.strptime(ls2, '%Y-%m-%dT%H:%M')
    # print(data)

    # hiddens = response.GET.get('hiddens')
    # print(hiddens+" is assumption")
    # cursor = connections['db.sqlite3'].cursor()
    # # cursor = connections['myworldtrial2'].cursor()
    # lsDates = cursor.execute('SELECT created_at FROM Reviews')
    # lsDates = Reviews.objects.raw('SELECT age(created_at) FROM Reviews')
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # db_path = os.path.join(BASE_DIR, "db.sqlite3")
    # with sqlite3.connect(db_path) as conn:
    #     # cursor = conn.cursor()
    #     # cursor.execute('SELECT created_at FROM main_reviews;')
    #     # data = cursor.fetchone()
    #     # print('SQLite version:', data)
    #     cursor = conn.cursor()
    #     cursor.execute("table")
    #     data = cursor.fetchone()
    #     print('SQLite version:', data)

    # print(lsDates)
    return render(response, "seeReview.html", {"ls": ls, "ls2": myPujas})


def book(response):
    myPujas = Puja.objects.all()
    return render(response, "book.html", {"items": myPujas})


def puja(request, id):
    if(request.method == 'POST'):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        yourRating = request.POST['yourRating']
        title = request.POST['title']
        your_reviews = request.POST['your_reviews']
        pujaName = Puja.objects.get(id=id)
        email = User.objects.get(username=request.user.username).email
        # print(email)
        myReviews = Reviews.objects.create(
            fullName=first_name+" "+last_name, title=title, pujaName=pujaName, email=email, yourRating=yourRating, reviewText=your_reviews)
        # print(myReviews+" saved!")
        myReviews.save()
        messages.info(request, 'Review created')
        return redirect("/seeReviews")
    else:
        ls = Puja.objects.get(id=id)
        ls2 = ls.nameOfPuja
        # ls3 = Puja.objects.all().aggregate(Avg('yourRating'))
        # print(ls3 + " is your rating")
        # Here pujaName = ls2 will not work, it'll give expected id but got Laxi Puja error
        # so to get a foreign key's filtering add foreignKey__nameOFCategory = ls2
        ls3 = Reviews.objects.filter(pujaName__nameOfPuja=ls2)
        ls3count = str(ls3.count())
        # print(ls3count + " ")
        # print(ls3)
        ls3Avg = ls3.aggregate(Avg('yourRating', output_field=FloatField()))
        # note - ls3Avg is a dictionary we have to put ls3Avg.yourRating__avg to get value
        # print(ls3Avg['yourRating__avg'])
        # when there is no review it is giving TypeError that no value can be of NoneType
        # so used exception handeling here
        # ls3AvgRoundoff2digit = 0.00
        while True:
            try:
                ls3AvgRoundoff2digit = round(ls3Avg['yourRating__avg'], 2)
                break
            except TypeError:
                # print("no reviews yet")
                ls3AvgRoundoff2digit = 0.00
                break
        # print(ls3AvgRoundoff2digit)
        # myls3Avg = ls3[:].yourRating__avg
        # myls3Avg = ls3.aggregate(Avg('yourRating'))
        # print(str(myls3Avg) + "is avarage")
        return render(request, "MahalaxmifullInfo.html", {"myPuja": ls2, "ls": ls, "ls3count": ls3count, "ls3Avg": ls3Avg, "ls3AvgRoundoff2digit": ls3AvgRoundoff2digit})


@login_required
def order(request, id):
    if request.method == 'POST':
        # ls = Puja.objects.get(id=id)
        # ls = ls.nameOfPuja
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['optradio']
        dateOfPuja = request.POST['birthdaytime']
        # print(gender)
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        address = address1 + ', ' + address2 + ', ' + city + ', ' + state + ', ' + zip
        # print(address)
        # total = '1000'
        email = User.objects.get(username=request.user.username).email
        # print(email)
        pujaName = Puja.objects.get(id=id)
        total = pujaName.price + 18  # 18rs are charges for transaction...
        mobile_no = request.POST['MobNo']
        # request.post se multiValueDictKey error aaya -> uske liye phir request.pits.get[] kiya
        # fir bhi error aaya ki TypeError: ‘method’ object is not subscriptable” iske liye brackets round kiye string
        # phir bhi can only concatenate str (not "NoneType") to str error aya uske liye " " kiya instead ''
        # orderRequestTime = request.POST['todayDate']
        # orderRequestTime = str(orderRequestTime)
        orderRequestTime = str(datetime.datetime.now())
        # print(type(orderRequestTime), orderRequestTime)
        #mobile_no = models.CharField(max_length=15)
        # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        # phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
        myOrder = Order.objects.create(
            first_name=first_name, last_name=last_name, mobile_no=mobile_no, pujaName=pujaName, dateOfPuja=dateOfPuja, address=address, email=email, total_pay=total, bookingDoneAt=orderRequestTime)
        myOrder.save()
        messages.info(request, 'Order successfully created')
        # for redirecting to myOrders page
        return redirect("payment")
        # return redirect(request.path)  # for redirecting to same page
        # return redirect("/")
        # return redirect("/puja/:<id>/order")
    else:
        # email = User.objects.get(username=request.user.username).email
        # print(email)
        # print(myPuja)
        ls = Puja.objects.get(id=id)
        # additionalCharges = 18
        # total_Charges = ls.price + additionalCharges
        # ls = ls.nameOfPuja
        # myPuja = Puja.objects.all()
        return render(request, "order.html", {"ls": ls})
        # return render(request, "order.html", {"myPuja": myPuja, "ls": ls})


@login_required
def payment(response):
    return render(response, "upi.html", {})


@login_required
def myOrders(request):
    # if 'myEditPuja' in request.POST:
    #     # SUBSCRIBE
    #     it = 17
    #     return redirect(request.path)
    # elif 'myCancellPuja' in request.POST:
    #     # UNSUBSCRIBE
    #     # orderList = Order.objects.filter(email=request.user.email)
    #     deletionId = request.POST.get('myUniqueValue')
    #     print(deletionId)
    #     # deletionElement = Order.objects.get(id=deletionId)
    #     # print(deletionElement)
    #     return redirect(request.path)
    # else:
    orderList = Order.objects.filter(email=request.user.email)
    # print(orderList)
    return render(request, "myOrders.html", {"orderList": orderList})


def updateOrders(request, pk):
    if request.method == 'POST':
        # ls = Puja.objects.get(id=id)
        # ls = ls.nameOfPuja
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dateOfPuja = request.POST['birthdaytime']
        # print(gender)
        address = request.POST['address']
        # print(address)
        # total = '1000'
        email = User.objects.get(username=request.user.username).email
        # print(email)
        pujaId = Order.objects.get(id=pk)
        pujaName = pujaId.pujaName
        total = pujaId.total_pay  # 18rs are charges for transaction...
        mobile_no = request.POST['MobNo']
        # request.post se multiValueDictKey error aaya -> uske liye phir request.pits.get[] kiya
        # fir bhi error aaya ki TypeError: ‘method’ object is not subscriptable” iske liye brackets round kiye string
        # phir bhi can only concatenate str (not "NoneType") to str error aya uske liye " " kiya instead ''
        # orderRequestTime = request.POST['todayDate']
        # orderRequestTime = str(orderRequestTime)
        orderRequestTime = str(datetime.datetime.now())
        # print(type(orderRequestTime), orderRequestTime)
        #mobile_no = models.CharField(max_length=15)
        # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        # phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
        Order.objects.filter(id=pk).update(
            first_name=first_name, last_name=last_name, mobile_no=mobile_no, pujaName=pujaName, dateOfPuja=dateOfPuja, address=address, email=email, total_pay=total, bookingDoneAt=orderRequestTime)
        # Order.objects.refresh_from_db()
        # Order.save()
        messages.info(request, 'Order successfully updated')
        # for redirecting to myOrders page
        return redirect("/myOrders")
    else:
        givenObject = Order.objects.get(id=pk)
        # form = OrderForm(request.POST)
        # abc = Order.objects.filter(id=givenObject.id)  # for filling up form
        # print(abc)
        date_time = givenObject.dateOfPuja
        # converting dd-mm-yyyy time of above object into y-m-d
        date_time = date_time.strftime("%Y-%m-%dT%H:%M:%S")
        print(date_time)
        # orderList = Order.objects.filter(email=request.user.email)
        return render(request, "updateOrder.html", {"ls": givenObject, "date_time": date_time})


def deleteOrders(request, pk):
    givenObject = Order.objects.get(id=pk)
    # if request.method == "POST":
    # print("deleting ", givenObject)
    givenObject.delete()
    # Order.save()
    orderList = Order.objects.filter(email=request.user.email)
    return render(request, "myOrders.html", {"orderList": orderList})


def pandit(response):
    # sortByField
    panditList = Pandit.objects.all()
    # print()
    pandits = Pandit.objects.all().values('panditDescription')
    #   <!-- since we have to  show manytomany fields we use this format to show it -->
    #   note that pujaName is a queryset as it is manytomany fields so we have to parse it in jinja template
    print((pandits))

    return render(response, "pandit.html", {"panditList": panditList})


def aboutUs(response):
    return render(response, "aboutUs.html", {})


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")
