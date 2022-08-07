from django.db import models
from django.contrib.auth.models import User
from jsonschema import ValidationError
from django import forms
from django.utils.timezone import now

# Create your models here.


def minMax(value):
    if(value < 0 or value > 90):
        raise ValidationError(
            ('Value must be between 0 and 90'), param={'value': value},)


def minMax2(value):
    if(value < 0 or value > 100000):
        raise ValidationError(
            ('Value must be between 0 and 1lakh'), param={'value': value},)


def minMax3(value):
    if(value < 0 or value > 5):
        raise ValidationError(
            ('Value must be between 0 and 5'), param={'value': value},)


expertiseField = (
    ('Mahalaxmi'),
    (''),
)

panditText = "One of the best Pandit available at panditMitra."

materials = (
    ('Flowers'),
    ('Beatle Leaves'),
    ('Mango Wood Sticks'),
    ('Aasan'),
    ('Cotton Wicks'),
    ('Ghee'),

)
# our_promise_options=(
#     ('For financial stability and gain'),
#     ('Done on friday or other auspicious days according to Nakshatra'),
#     ('Lotus flowers are main ingredients used'),
#     ('Other ingredients list will be provided separately after confirmation')
# )

# key_insights_options=(
#     ('Vedic pathshala certified Pandits'),
#     ('All pure ingredients used'),
#     ('On-time punctual poojas'),
#     ('Professional guidance and support'),
#     ('Custom changes to pooja are always Welcomed')
# )


# class pujaCat(models.Model):
#     catOfPuja = models.CharField(
#         primary_key=True, max_length=50)

#     def __str__(self):
#         return self.catOfPuja


class myUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    secretKey = models.IntegerField()
    # isPandit = models.BooleanField('is pandit', default=False)

class materialProvided(models.Model):
    id = models.AutoField(primary_key=True)
    materialName = models.CharField(max_length=100)

    def __str__(self):
        return self.materialName

class Puja(models.Model):
    id = models.AutoField(primary_key=True)
    nameOfPuja = models.CharField(max_length=50, unique=True)
    price = models.IntegerField(default=0, validators=[minMax2])
    # panditName = models.CharField(max_length=50, blank=True)    # imageURL textfield
    imageUrl = models.TextField(
        default="https://image.shutterstock.com/image-vector/vector-graphic-illustration-indian-pandit-260nw-1803127855.jpg", null=True, blank=True)
    # expertiseIn = models.Charfield(max_length=10, choices=expertiseField)
    introText = models.CharField(max_length=200, null=True, blank=True)
    discription = models.TextField(null=True, blank=True)
    # materials_provided = models.TextField(default=materials)
    # key_insights
    # our_promise = model
    # categories (Remove Late marriage/Wedding Obstacles) Puja,(Property/Legal/Court Cases) Shanti Puja,Sarpa Dosha Pooja,Swastha Sampanna Puja,Dussera,Laxmi Kubera,Mahalaxmi
    categories = models.CharField(max_length=50, blank=True, default="")
    subCategories = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return self.nameOfPuja
        # return "{}.{}".format(self.id, self.nameOfPuja)


class myPujaNnames(models.Model):
    id = models.AutoField(primary_key=True)
    pujassName = models.ManyToManyField(
        Puja, verbose_name="Puja names", blank=True)

    def __str__(self):
        return self.pujassName


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
    # bookingDoneAt = models.DateTimeField(auto_now_add=True,null=True)
    # time of request of order

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.pujaName} on {self.dateOfPuja} at {self.address}"


class Pandit(models.Model):
    id = models.AutoField(primary_key=True)
    imageUrl = models.TextField(verbose_name="Pandit Img Url", max_length=2000)
    # imageUrl = models.URLField(verbose_name="Pandit Img Url", max_length=2000)
    # nameOfPandit = models.ForeignKey(Puja, blank=True)
    nameOfPandit = models.CharField(max_length=50)
    experience = models.IntegerField(default=0, validators=[minMax])
    pujaNames = models.ManyToManyField(
        Puja, related_name="pujaNames1", blank=True, default=None)
    panditDescription = models.TextField(default=panditText)
    pujaAssigned = models.ManyToManyField(
        Order, blank=True, default=None, related_name="pujas")
    # pujaName = models.ForeignKey(Puja, on_delete=models.CASCADE)
    # pujaName = models.ForeignKey(Puja, on_delete=models.CASCADE)
    # expertiseIn = forms.ChoiceField(
    #     choices=expertise_choices, widget=forms.RadioSelect())
#   expertiseIn = models.CharFiels(max_length=200) fields add karni hai

    def __str__(self):
        return self.nameOfPandit


class Reviews(models.Model):
    id = models.AutoField(primary_key=True)
    fullName = models.CharField(max_length=50)
    pujaName = models.ForeignKey(Puja, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    title = models.CharField(max_length=50, blank=True)
    reviewText = models.TextField(verbose_name='Reviews Text')
    created_date = models.DateTimeField(default=now, editable=False)
    yourRating = models.IntegerField(default=0, validators=[minMax3])

    def __str__(self):
        return f"{self.created_date} {self.pujaName} {self.yourRating} stars {self.fullName}"
