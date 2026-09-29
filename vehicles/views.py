from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Vehicle, Appointment
from .forms import VehicleForm, AppointmentForm

def home(request):
    return render(request, 'vehicles/home.html')

@login_required
def dashboard(request):
    vehicles = Vehicle.objects.filter(owner=request.user)
    
    query = request.GET.get('q', '')
    if query:
        vehicles = vehicles.filter(
            Q(make__icontains=query) | 
            Q(model__icontains=query) | 
            Q(license_plate__icontains=query)
        )
        
    appointments = Appointment.objects.filter(vehicle__owner=request.user)
    
    total_vehicles = vehicles.count()
    total_appointments = appointments.count()
    try:
        pending_appointments = appointments.filter(status='pending').count()
    except:
        pending_appointments = 0
        
    context = {
        'vehicles': vehicles,
        'appointments': appointments,
        'total_vehicles': total_vehicles,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'query': query,
    }
    return render(request, 'vehicles/dashboard.html', context)

@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, 'Vehicle added successfully!')
            return redirect('dashboard')
    else:
        form = VehicleForm()
    return render(request, 'vehicles/add_vehicle.html', {'form': form})

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            messages.success(request, 'Maintenance appointment booked successfully!')
            return redirect('dashboard')
    else:
        form = AppointmentForm()
        form.fields['vehicle'].queryset = Vehicle.objects.filter(owner=request.user)
        
    return render(request, 'vehicles/book_appointment.html', {'form': form})

@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, vehicle__owner=request.user)
    if hasattr(appointment, 'status'):
        appointment.status = 'cancelled'
        appointment.save()
    else:
        appointment.delete()
    messages.warning(request, 'Appointment cancelled successfully!')
    return redirect('dashboard')