import datetime
from .models import Order, Pandit

def check_availibity(panditId, check_in, check_out):
    availability_list = []
    booking_list = Pandit.objects.filter(id = panditId)
    for booking in booking_list:
        if booking.check_in > check_out or booking.check_out < check_in:
            availability_list.append(True)
        else:
            availability_list.append(False)