from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id,
                'email': user.email,
                'first_name': user.first_name,
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        if User.objects.filter(email=data.get('email')).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
        )
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id,
            'email': user.email,
        }, status=status.HTTP_201_CREATED)

class BranchLocationsAPI(APIView):
    """Returns hardcoded branch locations for the map screen"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        branches = [
            {
                "name": "Depann Mo Loto - Main Branch",
                "address": "Port Louis, Mauritius",
                "lat": -20.1654,
                "lng": 57.4896,
                "phone": "+230 5000-0001",
                "hours": "Mon-Sat 8am-6pm"
            },
            {
                "name": "Depann Mo Loto - Curepipe",
                "address": "Curepipe, Mauritius",
                "lat": -20.3176,
                "lng": 57.5263,
                "phone": "+230 5000-0002",
                "hours": "Mon-Sat 8am-6pm"
            },
            {
                "name": "Depann Mo Loto - Rose Hill",
                "address": "Rose Hill, Mauritius",
                "lat": -20.2333,
                "lng": 57.4667,
                "phone": "+230 5000-0003",
                "hours": "Mon-Fri 8am-5pm"
            },
        ]
        return Response(branches)