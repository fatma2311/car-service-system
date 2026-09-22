from django.urls import path
from . import views

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),
    path('technicians/', views.technician_list, name='technician_list'),
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('appointments/', views.appointment_list, name='appointment_list'),
]