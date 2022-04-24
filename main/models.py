from django.db import models
from django.contrib.auth.models import User
from jsonschema import ValidationError
from django import forms

# Create your models here.


def minMax(value):
    if(value < 0 or value > 90):
        raise ValidationError(
            ('Value must be between 0 and 90'), param={'value': value},)


def minMax2(value):
    if(value < 0 or value > 100000):
        raise ValidationError(
            ('Value must be between 0 and 1lakh'), param={'value': value},)


class Puja(models.Model):
    id = models.AutoField(primary_key=True)
    nameOfPuja = models.CharField(max_length=50, unique=True)
    price = models.IntegerField(default=0, validators=[minMax2])
    panditName = models.CharField(max_length=50, blank=True)
    # categories (Remove Late marriage/Wedding Obstacles) Puja,(Property/Legal/Court Cases) Shanti Puja,Sarpa Dosha Pooja,Swastha Sampanna Puja,Dussera,Laxmi Kubera,Mahalaxmi

    def __str__(self):
        return self.nameOfPuja
        # return "{}.{}".format(self.id, self.nameOfPuja)


class Pandit(models.Model):
    id = models.AutoField(primary_key=True)
    imageUrl = models.TextField(verbose_name="Pandit Img Url", max_length=2000)
    # imageUrl = models.URLField(verbose_name="Pandit Img Url", max_length=2000)
    # nameOfPandit = models.ForeignKey(Puja, blank=True)
    nameOfPandit = models.CharField(max_length=50)
    experience = models.IntegerField(default=0, validators=[minMax])
    # pujaName = models.ForeignKey(Puja, on_delete=models.CASCADE)
    # expertiseIn = forms.ChoiceField(
    #     choices=expertise_choices, widget=forms.RadioSelect())
#   expertiseIn = models.CharFiels(max_length=200) fields add karni hai

    def __str__(self):
        return self.nameOfPandit


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # pujaId = models.ForeignKey(Puja, on_delete=models.CASCADE)
    pujaName = models.ForeignKey(Puja, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
    email = models.CharField(max_length=50)
    # email = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    dateOfPuja = models.DateTimeField()
    total_pay = models.CharField(max_length=50)
    bookingDoneAt = models.CharField(max_length=50)
    # time of request of order

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.pujaName} on {self.dateOfPuja} at {self.address}"
