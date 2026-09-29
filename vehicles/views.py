
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import (
    Vehicle,
    Technician,
    MaintenanceRecord,
    Appointment,
)

from .forms import VehicleForm, MaintenanceRecordForm, AppointmentForm


@login_required
def home(request):
    user = request.user

    if user.role == user.Role.CUSTOMER:
        vehicles = Vehicle.objects.filter(
            owner=user
        )

        maintenance_records = MaintenanceRecord.objects.filter(
            vehicle__owner=user
        )

        appointments = Appointment.objects.filter(
            vehicle__owner=user
        )

    elif user.role == user.Role.TECHNICIAN:
        vehicles = Vehicle.objects.filter(
            maintenance_records__technician__user=user
        ).distinct()

        maintenance_records = MaintenanceRecord.objects.filter(
            technician__user=user
        )

        appointments = Appointment.objects.filter(
            technician__user=user
        )

    elif user.role in [
        user.Role.ADMIN,
        user.Role.MANAGER,
    ]:
        vehicles = Vehicle.objects.all()

        maintenance_records = MaintenanceRecord.objects.all()

        appointments = Appointment.objects.all()

    else:
        vehicles = Vehicle.objects.none()
        maintenance_records = MaintenanceRecord.objects.none()
        appointments = Appointment.objects.none()

    today = timezone.localdate()

    due_services_count = 0

    for vehicle in vehicles:
        last_record = vehicle.maintenance_records.order_by(
            '-service_date'
        ).first()

        if (
            last_record
            and last_record.next_service_date
            and last_record.next_service_date <= today
        ):
            due_services_count += 1

    appointments_count = appointments.count()

    upcoming_appointments = appointments.filter(
        scheduled_date__gte=timezone.now(),
        status__in=[
            Appointment.Status.PENDING,
            Appointment.Status.CONFIRMED,
        ]
    ).order_by('scheduled_date')[:3]

    context = {
        'vehicles': vehicles,
        'vehicles_count': vehicles.count(),
        'maintenance_count': maintenance_records.count(),
        'appointments_count': appointments_count,
        'due_services_count': due_services_count,
        'upcoming_appointments': upcoming_appointments,
    }

    return render(
        request,
        'vehicles/home.html',
        context
    )


@login_required
def add_vehicle(request):
    if request.user.role != request.user.Role.CUSTOMER:
        return redirect('vehicle_list')

    if request.method == 'POST':
        form = VehicleForm(request.POST)

        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()

    return render(
        request,
        'vehicles/add_vehicle.html',
        {'form': form}
    )

@login_required
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id,
        owner=request.user,
    )

    if request.user.role != request.user.Role.CUSTOMER:
        return redirect('vehicle_list')

    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)

        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)

    return render(
        request,
        'vehicles/edit_vehicle.html',
        {'form': form, 'vehicle': vehicle}
    )

@login_required
def delete_vehicle(request, vehicle_id):
    if request.user.role != request.user.Role.CUSTOMER:
        return redirect('vehicle_list')

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id,
        owner=request.user,
    )

    if request.method == 'POST':
        vehicle.delete()

    return redirect('vehicle_list')

@login_required
def vehicle_list(request):
    user = request.user

    if user.role == user.Role.CUSTOMER:
        vehicles = Vehicle.objects.filter(
            owner=user
        )

    elif user.role == user.Role.TECHNICIAN:
        vehicles = Vehicle.objects.filter(
            maintenance_records__technician__user=user
        ).distinct()

    elif user.role in [
        user.Role.ADMIN,
        user.Role.MANAGER,
    ]:
        vehicles = Vehicle.objects.all()

    else:
        vehicles = Vehicle.objects.none()

    return render(
        request,
        'vehicles/vehicle_list.html',
        {
            'vehicles': vehicles
        }
    )


@login_required
def technician_list(request):
    if request.user.role not in [
        request.user.Role.ADMIN,
        request.user.Role.MANAGER,
    ]:
        return redirect('home')

    technicians = Technician.objects.all()

    return render(
        request,
        'vehicles/technician_list.html',
        {
            'technicians': technicians
        }
    )


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

    return render(
        request,
        'vehicles/maintenance_list.html',
        {
            'records': records
        }
    )

@login_required
def add_maintenance(request):
    if request.user.role not in [
        request.user.Role.ADMIN,
        request.user.Role.MANAGER,
        request.user.Role.TECHNICIAN,
    ]:
        return redirect('maintenance_list')

    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)

            if request.user.role == request.user.Role.TECHNICIAN:
                technician = get_object_or_404(
                    Technician,
                    user=request.user,
                )
                record.technician = technician

            record.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceRecordForm()

    return render(
        request,
        'vehicles/maintenance_form.html',
        {
            'form': form,
            'page_title': 'Add Maintenance Record',
            'submit_text': 'Add Record',
        }
    )


@login_required
def edit_maintenance(request, record_id):
    record = get_object_or_404(
        MaintenanceRecord,
        id=record_id,
    )

    user = request.user

    if user.role == user.Role.TECHNICIAN:
        if not record.technician or record.technician.user != user:
            return redirect('maintenance_list')

    elif user.role not in [
        user.Role.ADMIN,
        user.Role.MANAGER,
    ]:
        return redirect('maintenance_list')

    if request.method == 'POST':
        form = MaintenanceRecordForm(
            request.POST,
            instance=record,
        )

        if form.is_valid():
            updated_record = form.save(commit=False)

            if user.role == user.Role.TECHNICIAN:
                updated_record.technician = record.technician

            updated_record.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceRecordForm(instance=record)

    return render(
        request,
        'vehicles/maintenance_form.html',
        {
            'form': form,
            'page_title': 'Edit Maintenance Record',
            'submit_text': 'Save Changes',
            'record': record,
        }
    )


@login_required
def delete_maintenance(request, record_id):
    record = get_object_or_404(
        MaintenanceRecord,
        id=record_id,
    )

    user = request.user

    if user.role == user.Role.TECHNICIAN:
        if not record.technician or record.technician.user != user:
            return redirect('maintenance_list')

    elif user.role not in [
        user.Role.ADMIN,
        user.Role.MANAGER,
    ]:
        return redirect('maintenance_list')

    if request.method == 'POST':
        record.delete()

    return redirect('maintenance_list')

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

    elif user.role in [
        user.Role.ADMIN,
        user.Role.MANAGER,
    ]:
        appointments = Appointment.objects.all()

    else:
        appointments = Appointment.objects.none()

    appointments = appointments.order_by('scheduled_date')

    return render(
        request,
        'vehicles/appointment_list.html',
        {
            'appointments': appointments
        }
    )

@login_required
def cancel_appointment(request, appointment_id):
    if request.method != 'POST':
        return redirect('appointment_list')

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
    )

    user = request.user

    if user.role == user.Role.CUSTOMER:
        if appointment.vehicle.owner != user:
            return redirect('appointment_list')

    elif user.role == user.Role.TECHNICIAN:
        if not appointment.technician or appointment.technician.user != user:
            return redirect('appointment_list')

    elif user.role not in [
        user.Role.ADMIN,
        user.Role.MANAGER,
    ]:
        return redirect('appointment_list')

    if appointment.status == Appointment.Status.PENDING:
        appointment.status = Appointment.Status.CANCELLED
        appointment.save(update_fields=['status'])

    return redirect('appointment_list')

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
    )

    user = request.user

    if user.role == user.Role.CUSTOMER:
        if appointment.vehicle.owner != user:
            return redirect('appointment_list')

    elif user.role == user.Role.TECHNICIAN:
        if (
            not appointment.technician
            or appointment.technician.user != user
        ):
            return redirect('appointment_list')

    elif user.role not in [
        user.Role.ADMIN,
        user.Role.MANAGER,
    ]:
        return redirect('appointment_list')

    if request.method == 'POST':
        form = AppointmentForm(
            request.POST,
            instance=appointment,
        )

        if form.is_valid():
            updated_appointment = form.save(commit=False)

            if user.role == user.Role.CUSTOMER:
                updated_appointment.vehicle = appointment.vehicle
                updated_appointment.technician = appointment.technician
                updated_appointment.status = appointment.status

            elif user.role == user.Role.TECHNICIAN:
                updated_appointment.technician = appointment.technician

            updated_appointment.save()

            return redirect('appointment_list')

    else:
        form = AppointmentForm(
            instance=appointment
        )

    return render(
        request,
        'vehicles/appointment_form.html',
        {
            'form': form,
            'page_title': 'Edit Appointment',
            'submit_text': 'Save Changes',
            'appointment': appointment,
        }
    )


@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
    )

    user = request.user

    if user.role == user.Role.CUSTOMER:
        if appointment.vehicle.owner != user:
            return redirect('appointment_list')

    elif user.role == user.Role.TECHNICIAN:
        if (
            not appointment.technician
            or appointment.technician.user != user
        ):
            return redirect('appointment_list')

    elif user.role not in [
        user.Role.ADMIN,
        user.Role.MANAGER,
    ]:
        return redirect('appointment_list')

    if request.method == 'POST':
        appointment.delete()

    return redirect('appointment_list')

@login_required
def due_services(request):
    user = request.user

    if user.role == user.Role.CUSTOMER:
        vehicles = Vehicle.objects.filter(
            owner=user
        )

    elif user.role == user.Role.TECHNICIAN:
        vehicles = Vehicle.objects.filter(
            maintenance_records__technician__user=user
        ).distinct()

    else:
        vehicles = Vehicle.objects.all()

    due_services = []
    today = timezone.localdate()

    for vehicle in vehicles:
        last_record = vehicle.maintenance_records.order_by(
            '-service_date'
        ).first()

        if last_record and last_record.next_service_date:
            if last_record.next_service_date < today:
                status = 'Overdue'
            elif last_record.next_service_date <= (
                today + timezone.timedelta(days=7)
            ):
                status = 'Due Soon'
            else:
                status = 'Up to Date'

            if status != 'Up to Date':
                due_services.append({
                    'vehicle': vehicle,
                    'record': last_record,
                    'status': status,
                })

    return render(
        request,
        'vehicles/due_services.html',
        {
            'due_services': due_services
        }
    )

