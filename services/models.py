# Create your models here.

from django.db import models

class Service(models.Model):
    SERVICE_TYPES = [
        ('car_servicing', 'Car Servicing'),
        ('battery_check', 'Battery Check'),
        ('mechanical_repair', 'Mechanical Repair'),
        ('tyre_replacement', 'Tyre Replacement'),
        ('ac_service', 'AC Service'),
        ('preventive_maintenance', 'Preventive Maintenance'),
    ]
    
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=50)
    is_popular = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Automatically set the name based on service_type
        self.name = dict(self.SERVICE_TYPES).get(self.service_type, self.service_type)
        super().save(*args, **kwargs)