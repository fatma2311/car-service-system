
from django.contrib import admin

from .models import Technician, Vehicle, MaintenanceRecord, Appointment


admin.site.register(Technician)
admin.site.register(Vehicle)


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = (
        'vehicle',
        'service_date',
        'next_service_date',
        'status',
        'technician',
        'cost',
    )

    list_filter = (
        'status',
        'service_date',
        'next_service_date',
    )


admin.site.register(Appointment)
