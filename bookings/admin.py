from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Vehicle, Booking
from services.models import Service

class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'customer_name', 'vehicle_info', 'service_name', 'service_price', 'booking_date', 'preferred_time', 'status', 'status_badge']
    list_filter = ['status', 'booking_date', 'service']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'vehicle__make', 'vehicle__model', 'vehicle__license_plate']
    list_editable = ['status']  # Now 'status' is in list_display
    readonly_fields = ['created_at', 'updated_at', 'status_badge']
    date_hierarchy = 'booking_date'
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('user', 'vehicle', 'service', 'booking_date', 'preferred_time')
        }),
        ('Status & Details', {
            'fields': ('status', 'status_badge', 'special_requests')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def booking_id(self, obj):
        return f"#{obj.id}"
    booking_id.short_description = 'ID'
    
    def customer_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    customer_name.short_description = 'Customer'
    customer_name.admin_order_field = 'user__first_name'
    
    def vehicle_info(self, obj):
        return f"{obj.vehicle.year} {obj.vehicle.make} {obj.vehicle.model}"
    vehicle_info.short_description = 'Vehicle'
    
    def service_name(self, obj):
        return obj.service.name
    service_name.short_description = 'Service'
    
    def service_price(self, obj):
        return f"Rs {obj.service.price}"
    service_price.short_description = 'Price'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'blue', 
            'in_progress': 'purple',
            'completed': 'green',
            'cancelled': 'red'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status Badge'

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['license_plate', 'vehicle_info', 'owner_name', 'owner_email', 'vehicle_type', 'vin']
    list_filter = ['vehicle_type', 'year']
    search_fields = ['license_plate', 'make', 'model', 'user__email', 'user__first_name', 'user__last_name', 'vin']
    
    def vehicle_info(self, obj):
        return f"{obj.year} {obj.make} {obj.model}"
    vehicle_info.short_description = 'Vehicle'
    
    def owner_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    owner_name.short_description = 'Owner'
    
    def owner_email(self, obj):
        return obj.user.email
    owner_email.short_description = 'Email'

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'description_short']
    list_editable = ['price', 'duration']
    search_fields = ['name', 'description']
    
    def description_short(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'

# Custom User Admin for better customer management
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'date_joined', 'is_staff', 'booking_count']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    
    def booking_count(self, obj):
        return obj.booking_set.count()
    booking_count.short_description = 'Bookings'

# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models
admin.site.register(Booking, BookingAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Service, ServiceAdmin)

# Customize admin site header
admin.site.site_header = "Depann Mo Loto Administration"
admin.site.site_title = "Depann Mo Loto Admin"
admin.site.index_title = "Welcome to Depann Mo Loto Admin Portal"