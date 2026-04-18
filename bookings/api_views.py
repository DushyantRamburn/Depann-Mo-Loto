from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking, Vehicle
from .serializers import BookingSerializer, VehicleSerializer
from services.models import Service
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone

User = get_user_model()

class UserBookingsAPI(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')

class CreateBookingAPI(APIView):
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
            # Parse the datetime string
            booking_datetime = datetime.strptime(
                data['booking_date'], '%Y-%m-%d %H:%M:%S'
            )
            # Make it timezone-aware
            booking_datetime = timezone.make_aware(booking_datetime)

            booking = Booking.objects.create(
                user=request.user,
                vehicle=vehicle,
                service=service,
                booking_date=booking_datetime,
                preferred_time=booking_datetime.time(),
                status='pending'
            )
            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        except Service.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response({'error': f'Missing field: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'error': f'Invalid date format: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CancelBookingAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
            booking.status = 'cancelled'
            booking.save()
            return Response({'message': 'Booking cancelled'})
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        
class UpdateBookingAPI(APIView):
    """Update a booking status"""
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
            new_status = request.data.get('status', booking.status)
            valid_statuses = ['pending', 'confirmed', 'in_progress', 'completed', 'cancelled']
            if new_status not in valid_statuses:
                return Response(
                    {'error': 'Invalid status'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            booking.status = new_status
            booking.save()
            return Response(BookingSerializer(booking).data)
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class DeleteBookingAPI(APIView):
    """Delete a booking"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
            booking.delete()
            return Response(
                {'message': 'Booking deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )