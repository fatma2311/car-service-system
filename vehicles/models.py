from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=50, verbose_name="Make")
    model = models.CharField(max_length=50, verbose_name="Model")
    year = models.IntegerField(verbose_name="Manufacturing Year")
    license_plate = models.CharField(max_length=20, unique=True, verbose_name="License Plate")
    mileage = models.IntegerField(verbose_name="Mileage (KM)", default=0)

    def get_service_recommendation(self):
        current_year = timezone.now().year
        age = current_year - self.year
        if age > 5:
            return "Recommendation: Comprehensive engine and brake inspection (Older vehicle)."
        elif age > 2:
            return "Recommendation: Regular oil and filter change."
        else:
            return "Recommendation: Routine general inspection."

    def str(self):
        return f"{self.make} {self.model} ({self.license_plate})"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='appointments', verbose_name="Vehicle")
    appointment_date = models.DateTimeField(verbose_name="Appointment Date & Time")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Status")

    def clean(self):
        if self.appointment_date and self.appointment_date < timezone.now():
            raise ValidationError({'appointment_date': "Cannot book an appointment in a past date or time."})

    def str(self):
        return f"Appointment for {self.vehicle.make} - {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"