# depann_mo_loto/api_urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.api_views import LoginAPI, RegisterAPI, BranchLocationsAPI
from services.api_views import ServiceListAPI, ServiceDetailAPI
from bookings.api_views import UserBookingsAPI, CreateBookingAPI, CancelBookingAPI, UpdateBookingAPI, DeleteBookingAPI

urlpatterns = [
    # Auth
    path('auth/login/', LoginAPI.as_view(), name='api-login'),
    path('auth/register/', RegisterAPI.as_view(), name='api-register'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    # Services
    path('services/', ServiceListAPI.as_view(), name='api-services'),
    path('services/<int:pk>/', ServiceDetailAPI.as_view(), name='api-service-detail'),
    # Bookings
    path('bookings/', UserBookingsAPI.as_view(), name='api-bookings'),
    path('bookings/create/', CreateBookingAPI.as_view(), name='api-create-booking'),
    path('bookings/<int:pk>/cancel/', CancelBookingAPI.as_view(), name='api-cancel-booking'),
    path('bookings/<int:pk>/update/', UpdateBookingAPI.as_view(), name='api-update-booking'),
    path('bookings/<int:pk>/delete/', DeleteBookingAPI.as_view(), name='api-delete-booking'),
    # Locations
    path('branches/', BranchLocationsAPI.as_view(), name='api-branches'),
]