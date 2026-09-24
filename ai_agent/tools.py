from vehicles.models import Vehicle, Technician, Appointment
from django.utils import timezone
from django.utils.dateparse import parse_datetime

def get_maintenance_history(license_plate: str) -> str:
    """Get the full maintenance history for a specific vehicle using its license plate.

    Args:
        license_plate: The vehicle's license plate number, e.g. ABC-1234.
    """
    try:
        vehicle = Vehicle.objects.get(license_plate__iexact=license_plate)
    except Vehicle.DoesNotExist:
        return f"No vehicle found with license plate {license_plate}."

    records = vehicle.maintenance_records.all().order_by('-service_date')
    if not records:
        return f"No maintenance records found for {vehicle}."

    lines = [
        f"- {r.service_date}: {r.description} (Status: {r.status}, Cost: {r.cost} EGP)"
        for r in records
    ]
    return f"Maintenance history for {vehicle}:\n" + "\n".join(lines)


def get_available_technicians() -> str:
    """Get the list of technicians who are currently available to take new work."""
    techs = Technician.objects.filter(is_available=True)
    if not techs:
        return "No technicians are currently available."
    return "Available technicians:\n" + "\n".join(
        f"- {t.user.username} (Specialty: {t.specialty})" for t in techs
    )


def make_book_appointment_tool(user):
    """Creates a booking tool that knows which user is making the request."""

    def book_appointment(license_plate: str, scheduled_date: str, notes: str = "") -> str:
        """Book a maintenance appointment for a vehicle with the first available technician.

        Args:
            license_plate: The vehicle's license plate, e.g. ABC-1234.
            scheduled_date: Date and time in the format YYYY-MM-DD HH:MM, e.g. 2026-09-25 10:00.
            notes: Optional notes about what the appointment is for.
        """
        try:
            vehicle = Vehicle.objects.get(license_plate__iexact=license_plate)
        except Vehicle.DoesNotExist:
            return f"No vehicle found with license plate {license_plate}."

        if user.role == user.Role.CUSTOMER and vehicle.owner_id != user.id:
            return "You are not authorized to book an appointment for this vehicle."

        technician = Technician.objects.filter(is_available=True).first()
        if not technician:
            return "No technicians are currently available."

        dt = parse_datetime(scheduled_date)
        if dt is None:
            return "Could not understand that date/time. Please use the format YYYY-MM-DD HH:MM."
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)

        appt = Appointment.objects.create(
            vehicle=vehicle,
            technician=technician,
            scheduled_date=dt,
            notes=notes,
        )
        return (
            f"Appointment booked successfully for {vehicle} "
            f"with technician {technician.user.username} on {appt.scheduled_date}. "
            f"Status: {appt.status}."
        )

    return book_appointment


def make_cancel_appointment_tool(user):
    """Creates a cancellation tool that knows which user is making the request."""

    def cancel_appointment(license_plate: str, scheduled_date: str) -> str:
        """Cancel an existing pending appointment for a vehicle.

        Args:
            license_plate: The vehicle's license plate, e.g. ABC-1234.
            scheduled_date: The date and time of the appointment to cancel, format YYYY-MM-DD HH:MM.
        """
        try:
            vehicle = Vehicle.objects.get(license_plate__iexact=license_plate)
        except Vehicle.DoesNotExist:
            return f"No vehicle found with license plate {license_plate}."

        if user.role == user.Role.CUSTOMER and vehicle.owner_id != user.id:
            return "You are not authorized to cancel appointments for this vehicle."

        dt = parse_datetime(scheduled_date)
        if dt is None:
            return "Could not understand that date/time. Please use the format YYYY-MM-DD HH:MM."
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)

        appointment = Appointment.objects.filter(
            vehicle=vehicle,
            scheduled_date=dt,
            status=Appointment.Status.PENDING,
        ).first()

        if not appointment:
            return "No matching pending appointment found for that date and time."

        appointment.status = Appointment.Status.CANCELLED
        appointment.save()
        return f"Appointment for {vehicle} on {appointment.scheduled_date} has been cancelled."

    return cancel_appointment