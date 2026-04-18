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
        User = get_user_model()

        if User.objects.filter(email=data.get('email')).exists():
            return Response(
                {'error': 'Email already registered'},
                status=status.HTTP_400_BAD_REQUEST
            )

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
    """Returns branch locations — consumed by both web (jQuery AJAX) and mobile (Flet)"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        branches = [
            {
                "name": "Vacoas Branch",
                "address": "123 Royal Road, Vacoas",
                "lat": -20.3176,
                "lng": 57.4845,
                "phone": "+230 686 1234",
                "hours": "Mon-Sat 8am-6pm"
            },
            {
                "name": "Port Louis Branch",
                "address": "456 Sir William Newton Street, Port Louis",
                "lat": -20.1654,
                "lng": 57.4896,
                "phone": "+230 212 5678",
                "hours": "Mon-Sat 8am-6pm"
            },
            {
                "name": "Flacq Branch",
                "address": "789 Royal Road, Centre de Flacq",
                "lat": -20.1833,
                "lng": 57.7167,
                "phone": "+230 413 9012",
                "hours": "Mon-Fri 8am-5pm"
            },
            {
                "name": "Goodlands Branch",
                "address": "321 Royal Road, Goodlands",
                "lat": -19.9833,
                "lng": 57.6500,
                "phone": "+230 283 4567",
                "hours": "Mon-Fri 8am-5pm"
            },
        ]
        return Response(branches)