from django.urls import path
from . import views

app_name = 'services'  # This creates the 'services' namespace

urlpatterns = [
    path('', views.services_list, name='list'),
]
