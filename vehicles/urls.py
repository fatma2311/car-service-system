from django.urls import path
from . import views

urlpatterns = [
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('technicians/', views.technician_list, name='technician_list'),
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path(
    'appointments/<int:appointment_id>/cancel/',
    views.cancel_appointment,
    name='cancel_appointment'
),
    path('due-services/', views.due_services, name='due_services'),
]