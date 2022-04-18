from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Puja(models.Model):
    id = models.AutoField(primary_key=True)
    nameOfPuja = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "{}.{}".format(self.id, self.nameOfPuja)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # pujaId = models.ForeignKey(Puja, on_delete=models.CASCADE)
    pujaName = models.ForeignKey(Puja, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    dateOfPuja = models.DateTimeField()
    total_pay = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.pujaName} {self.dateOfPuja} {self.address}"
