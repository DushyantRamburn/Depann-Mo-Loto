from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking, Vehicle
from .serializers import BookingSerializer, VehicleSerializer
from services.models import Service
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBookingsAPI(generics.ListAPIView):
    """Get all bookings for the logged-in user"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')

class CreateBookingAPI(APIView):
    """Create a new booking from the mobile app"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            service = Service.objects.get(id=data['service_id'])
            vehicle, _ = Vehicle.objects.get_or_create(
                user=request.user,
                license_plate=data['license_plate'],
                defaults={
                    'make': data['make'],
                    'model': data['model'],
                    'year': data['year'],
                    'vehicle_type': data.get('vehicle_type', 'car'),
                }
            )
            booking = Booking.objects.create(
                user=request.user,
                vehicle=vehicle,
                service=service,
                booking_date=data['booking_date'],
                status='pending'
            )
            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        except Service.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response({'error': f'Missing field: {e}'}, status=status.HTTP_400_BAD_REQUEST)

class CancelBookingAPI(APIView):
    """Cancel a booking"""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
            booking.status = 'cancelled'
            booking.save()
            return Response({'message': 'Booking cancelled'})
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)