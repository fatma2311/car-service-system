from django.contrib import admin
from .models import Technician, Vehicle, MaintenanceRecord, Appointment

admin.site.register(Technician)
admin.site.register(Vehicle)
admin.site.register(MaintenanceRecord)
admin.site.register(Appointment)