from django import forms
from .models import Vehicle
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ServiceSelectionForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=None,  # Will set in view
        empty_label="Select a service",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'license_plate', 'vehicle_type', 'vin']
        widgets = {
            'make': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Toyota'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Corolla'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2020', 'min': '1990', 'max': '2030'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., AB12345'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'vin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional VIN number'}),
        }

class DateTimeSelectionForm(forms.Form):
    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    preferred_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    special_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requests or notes about your vehicle...'})
    )

class PersonalDetailsForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your first name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your last name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+230 5XXX XXXX'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update widget attributes for all fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Create a strong password',
            'autocomplete': 'new-password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password'
        })
        
        # Remove help text that might confuse users
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")
        
        return cleaned_data