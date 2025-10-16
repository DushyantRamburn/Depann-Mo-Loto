from django.core.management.base import BaseCommand
from services.models import Service

class Command(BaseCommand):
    help = 'Seed the database with the 6 specific services'
    
    def handle(self, *args, **kwargs):
        services_data = [
            {
                'service_type': 'car_servicing',
                'description': 'Complete car servicing including oil change, filter replacement, and comprehensive vehicle inspection',
                'price': 2500.00,
                'duration': '2-3 hours',
                'is_popular': True
            },
            {
                'service_type': 'battery_check',
                'description': 'Professional battery testing, cleaning, and replacement if needed',
                'price': 800.00,
                'duration': '30-45 mins',
                'is_popular': False
            },
            {
                'service_type': 'mechanical_repair',
                'description': 'Expert mechanical repairs for engine, transmission, and other critical components',
                'price': 1500.00,
                'duration': '2-4 hours',
                'is_popular': True
            },
            {
                'service_type': 'tyre_replacement',
                'description': 'Complete tyre replacement service including wheel balancing and alignment',
                'price': 3000.00,
                'duration': '1-2 hours',
                'is_popular': False
            },
            {
                'service_type': 'ac_service',
                'description': 'AC system cleaning, gas refill, and performance optimization',
                'price': 1200.00,
                'duration': '1-1.5 hours',
                'is_popular': True
            },
            {
                'service_type': 'preventive_maintenance',
                'description': 'Proactive maintenance to prevent future issues and extend vehicle life',
                'price': 3000.00,
                'duration': '3-4 hours',
                'is_popular': False
            },
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                service_type=service_data['service_type'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f"Created service: {service.name}")
            else:
                self.stdout.write(f"Service already exists: {service.name}")
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded all 6 services')
        )