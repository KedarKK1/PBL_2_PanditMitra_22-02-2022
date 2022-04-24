from django.contrib import admin
from .models import Order, Puja, Pandit
# Register your models here.
admin.site.register(Puja)
admin.site.register(Order)
admin.site.register(Pandit)
