from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Booking, Vehicle
from .forms import ServiceSelectionForm, VehicleForm, DateTimeSelectionForm, PersonalDetailsForm

def booking_start(request):
    """Frame 1: Service Selection"""
    from services.models import Service
    
    service_type = request.GET.get('service')
    initial_service = None
    
    if service_type:
        try:
            initial_service = Service.objects.get(service_type=service_type)
        except Service.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = ServiceSelectionForm(request.POST)
        form.fields['service'].queryset = Service.objects.all()  # Show all services
        if form.is_valid():
            service_id = form.cleaned_data['service'].id
            request.session['booking_data'] = {
                'service_id': service_id
            }
            return redirect('bookings:vehicle_details')
    else:
        form = ServiceSelectionForm(initial={'service': initial_service} if initial_service else None)
        form.fields['service'].queryset = Service.objects.all()  # Show all services
    
    services = Service.objects.all()  # Show all services
    return render(request, 'bookings/booking_frame1.html', {
        'form': form,
        'services': services,
        'preselected_service': initial_service
    })

def vehicle_details(request):
    """Frame 2: Vehicle Details"""
    if 'booking_data' not in request.session:
        return redirect('bookings:booking_start')
    
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            # Store vehicle data in session
            request.session['booking_data']['vehicle'] = {
                'make': form.cleaned_data['make'],
                'model': form.cleaned_data['model'],
                'year': form.cleaned_data['year'],
                'license_plate': form.cleaned_data['license_plate'],
                'vehicle_type': form.cleaned_data['vehicle_type'],
                'vin': form.cleaned_data['vin'],
            }
            # Force session save
            request.session.save()
            print("Vehicle saved to session")
            return redirect('bookings:datetime_selection')
    else:
        form = VehicleForm()
    
    return render(request, 'bookings/booking_frame2.html', {'form': form})

def datetime_selection(request):
    """Frame 3: Date and Time Selection"""
    if 'booking_data' not in request.session:
        return redirect('bookings:booking_start')
    
    if request.method == 'POST':
        form = DateTimeSelectionForm(request.POST)
        if form.is_valid():
            # Convert to strings for session storage
            booking_date = form.cleaned_data['booking_date']
            preferred_time = form.cleaned_data['preferred_time']
            
            request.session['booking_data']['datetime'] = {
                'booking_date': booking_date.isoformat(),  # Convert to ISO string
                'preferred_time': preferred_time.isoformat(),  # Convert to ISO string
                'special_requests': form.cleaned_data['special_requests'],
            }
            request.session.modified = True
            return redirect('bookings:personal_details')
    else:
        form = DateTimeSelectionForm()
    
    return render(request, 'bookings/booking_frame3.html', {'form': form})

def personal_details(request):
    """Frame 4: Personal Details and Account Creation"""
    if 'booking_data' not in request.session:
        return redirect('bookings:booking_start')
    
    booking_data = request.session['booking_data']
    
    if 'service_id' not in booking_data:
        return redirect('bookings:booking_start')
    elif 'vehicle' not in booking_data:
        return redirect('bookings:vehicle_details')
    elif 'datetime' not in booking_data:
        return redirect('bookings:datetime_selection')
    
    if request.method == 'POST':
        form = PersonalDetailsForm(request.POST)
        if form.is_valid():
            try:
                # Create user account
                user = form.save(commit=False)
                user.username = form.cleaned_data['email']
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()
                
                # Create vehicle
                vehicle_data = booking_data['vehicle']
                vehicle = Vehicle.objects.create(
                    user=user,
                    **vehicle_data
                )
                
                # Create booking - convert ISO strings back to objects
                from services.models import Service
                from datetime import datetime, date, time
                datetime_data = booking_data['datetime']
                
                # Convert ISO string back to date object
                booking_date = date.fromisoformat(datetime_data['booking_date'])
                # Convert ISO string back to time object
                preferred_time = time.fromisoformat(datetime_data['preferred_time'])
                
                booking = Booking.objects.create(
                    user=user,
                    vehicle=vehicle,
                    service_id=booking_data['service_id'],
                    booking_date=booking_date,
                    preferred_time=preferred_time,
                    special_requests=datetime_data['special_requests']
                )
                
                # Log the user in
                from django.contrib.auth import login
                login(request, user)
                
                # Clear session data
                if 'booking_data' in request.session:
                    del request.session['booking_data']
                
                return redirect('bookings:booking_summary', booking_id=booking.id)
                
            except Exception as e:
                return render(request, 'bookings/booking_frame4.html', {
                    'form': form,
                    'error': f'Error creating account: {str(e)}'
                })
        else:
            print("Form errors:", form.errors)
    else:
        form = PersonalDetailsForm()
    
    return render(request, 'bookings/booking_frame4.html', {'form': form})

@login_required
def booking_summary(request, booking_id):
    """Booking Summary Page"""
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return redirect('pages:home')
    
    return render(request, 'bookings/booking_summary.html', {'booking': booking})

def booking_success(request):
    """Simple success page"""
    return render(request, 'bookings/booking_success.html')
