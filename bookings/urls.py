
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('start/', views.booking_start, name='booking_start'),
    path('create/', views.booking_start, name='create'),
    path('vehicle/', views.vehicle_details, name='vehicle_details'),
    path('datetime/', views.datetime_selection, name='datetime_selection'),
    path('personal/', views.personal_details, name='personal_details'),
    path('summary/<int:booking_id>/', views.booking_summary, name='booking_summary'),
    path('success/', views.booking_success, name='booking_success'),
]


