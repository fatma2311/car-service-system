from django.shortcuts import render
from .models import Vehicle, Technician, MaintenanceRecord, Appointment

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicles/vehicle_list.html', {'vehicles': vehicles})


def technician_list(request):
    technicians = Technician.objects.all()
    return render(request, 'vehicles/technician_list.html', {'technicians': technicians})


def maintenance_list(request):
    records = MaintenanceRecord.objects.all().order_by('-service_date')
    return render(request, 'vehicles/maintenance_list.html', {'records': records})


def appointment_list(request):
    appointments = Appointment.objects.all().order_by('scheduled_date')
    return render(request, 'vehicles/appointment_list.html', {'appointments': appointments})

