
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('new/', views.booking_create, name='create'),
]


