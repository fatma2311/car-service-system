from django import forms
from .models import Vehicle, MaintenanceRecord, Appointment


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'license_plate']


class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = [
            'vehicle',
            'technician',
            'description',
            'status',
            'service_date',
            'next_service_date',
            'cost',
        ]

        widgets = {
            'service_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'next_service_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'description': forms.Textarea(
                attrs={'rows': 4}
            ),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'vehicle',
            'technician',
            'scheduled_date',
            'status',
            'notes',
        ]

        widgets = {
            'scheduled_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 4
                }
            ),
        }