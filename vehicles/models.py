from django.db import models
from django.conf import settings


class Technician(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='technician_profile'
    )
    specialty = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.specialty}"


class Vehicle(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"


class MaintenanceRecord(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='maintenance_records'
    )

    technician = models.ForeignKey(
        Technician,
        on_delete=models.SET_NULL,
        null=True,
        related_name='maintenance_records'
    )

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )

    service_date = models.DateField()

    next_service_date = models.DateField(
        null=True,
        blank=True
    )

    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.vehicle} - {self.service_date} ({self.status})"


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    technician = models.ForeignKey(
        Technician,
        on_delete=models.SET_NULL,
        null=True,
        related_name='appointments'
    )
    scheduled_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.vehicle} @ {self.scheduled_date} ({self.status})"