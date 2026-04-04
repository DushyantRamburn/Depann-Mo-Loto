from rest_framework import generics, permissions
from .models import Service
from .serializers import ServiceSerializer

class ServiceListAPI(generics.ListAPIView):
    """Public endpoint - list all services"""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]

class ServiceDetailAPI(generics.RetrieveAPIView):
    """Public endpoint - get one service"""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]