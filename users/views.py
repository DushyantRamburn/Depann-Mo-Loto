from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from bookings.models import Booking, Vehicle

def login_view(request):
    """User login view"""
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                next_url = request.GET.get('next', 'users:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def register(request):
    """Registration view - redirect to booking since registration happens during booking"""
    messages.info(request, 'To create an account, please book a service first.')
    return redirect('bookings:create')

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('pages:home')

@login_required
def dashboard(request):
    """User dashboard with bookings and profile"""
    # Get user's bookings ordered by date (newest first)
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    
    # Get user's vehicles
    vehicles = Vehicle.objects.filter(user=request.user)
    
    # Use today's date for comparison
    from datetime import date
    today = date.today()
    
    # Filter bookings using database queries (more efficient)
    upcoming_bookings = bookings.filter(booking_date__gte=today)
    past_bookings = bookings.filter(booking_date__lt=today)
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'vehicles': vehicles,
    }
    
    return render(request, 'users/dashboard.html', context)

@login_required
def booking_detail(request, booking_id):
    """Detailed view of a specific booking"""
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('users:dashboard')
    
    return render(request, 'users/booking_detail.html', {'booking': booking})
