from django.urls import path
from . import views

urlpatterns = [
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path(
    'vehicles/<int:vehicle_id>/edit/',
    views.edit_vehicle,
    name='edit_vehicle'
),
path(
    'vehicles/<int:vehicle_id>/delete/',
    views.delete_vehicle,
    name='delete_vehicle'
),
    path('technicians/', views.technician_list, name='technician_list'),
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path(
    'maintenance/add/',
    views.add_maintenance,
    name='add_maintenance'
),
path(
    'maintenance/<int:record_id>/edit/',
    views.edit_maintenance,
    name='edit_maintenance'
),
path(
    'maintenance/<int:record_id>/delete/',
    views.delete_maintenance,
    name='delete_maintenance'
),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path(
    'appointments/<int:appointment_id>/cancel/',
    views.cancel_appointment,
    name='cancel_appointment'
),
path(
    'appointments/<int:appointment_id>/edit/',
    views.edit_appointment,
    name='edit_appointment'
),
path(
    'appointments/<int:appointment_id>/delete/',
    views.delete_appointment,
    name='delete_appointment'
),
    path('due-services/', views.due_services, name='due_services'),
]