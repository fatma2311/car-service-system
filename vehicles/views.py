
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Vehicle, Technician, MaintenanceRecord, Appointment


def home(request):
    return render(request, 'vehicles/home.html')


@login_required
def vehicle_list(request):
    user = request.user

    if user.role == user.Role.CUSTOMER:
        vehicles = Vehicle.objects.filter(owner=user)
    else:
        vehicles = Vehicle.objects.all()

    return render(request, 'vehicles/vehicle_list.html', {
        'vehicles': vehicles
    })


@login_required
def technician_list(request):
    technicians = Technician.objects.all()

    return render(request, 'vehicles/technician_list.html', {
        'technicians': technicians
    })


@login_required
def maintenance_list(request):
    user = request.user

    if user.role == user.Role.CUSTOMER:
        records = MaintenanceRecord.objects.filter(
            vehicle__owner=user
        )

    elif user.role == user.Role.TECHNICIAN:
        records = MaintenanceRecord.objects.filter(
            technician__user=user
        )

    else:
        records = MaintenanceRecord.objects.all()

    records = records.order_by('-service_date')

    return render(request, 'vehicles/maintenance_list.html', {
        'records': records
    })


@login_required
def appointment_list(request):
    user = request.user

    if user.role == user.Role.CUSTOMER:
        appointments = Appointment.objects.filter(
            vehicle__owner=user
        )

    elif user.role == user.Role.TECHNICIAN:
        appointments = Appointment.objects.filter(
            technician__user=user
        )

    else:
        appointments = Appointment.objects.all()

    appointments = appointments.order_by('scheduled_date')

    return render(request, 'vehicles/appointment_list.html', {
        'appointments': appointments
    })

