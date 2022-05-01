from django.contrib import admin
from .models import Order, Puja, Pandit, Reviews, myUser
# Register your models here.
admin.site.register(Puja)
admin.site.register(Order)
admin.site.register(Pandit)
admin.site.register(Reviews)
admin.site.register(myUser)
