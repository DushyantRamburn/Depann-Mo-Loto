from django.shortcuts import render

# Create your views here.

def booking_create(request):
    return render(request, 'bookings/booking_form.html')


