from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        TECHNICIAN = 'TECHNICIAN', 'Technician'
        CUSTOMER = 'CUSTOMER', 'Customer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"