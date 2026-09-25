from vehicles.models import Vehicle, Technician, Appointment
from django.utils import timezone
from django.utils.dateparse import parse_datetime


def make_get_my_vehicles_tool(user):
    """Get all vehicles owned by the current user."""

    def get_my_vehicles() -> str:
        """Get the vehicles that belong to the currently logged-in user."""

        if user.role == user.Role.CUSTOMER:
            vehicles = Vehicle.objects.filter(owner=user)
        else:
            vehicles = Vehicle.objects.all()

        if not vehicles.exists():
            return "No vehicles found for this user."

        lines = []

        for vehicle in vehicles:
            lines.append(
                f"- {vehicle.license_plate}: {vehicle}"
            )

        return "User's vehicles:\n" + "\n".join(lines)

    return get_my_vehicles


def make_get_maintenance_history_tool(user):
    """Get maintenance history only for vehicles accessible to the current user."""

    def get_maintenance_history(license_plate: str) -> str:
        """Get the full maintenance history for a specific vehicle."""

        try:
            vehicle = Vehicle.objects.get(
                license_plate__iexact=license_plate
            )
        except Vehicle.DoesNotExist:
            return f"No vehicle found with license plate {license_plate}."

        if (
            user.role == user.Role.CUSTOMER
            and vehicle.owner_id != user.id
        ):
            return "You are not authorized to view maintenance history for this vehicle."

        records = vehicle.maintenance_records.all().order_by(
            "-service_date"
        )

        if not records.exists():
            return f"No maintenance records found for {vehicle}."

        lines = [
            f"- {r.service_date}: {r.description} "
            f"(Status: {r.status}, Cost: {r.cost} EGP)"
            for r in records
        ]

        return (
            f"Maintenance history for {vehicle}:\n"
            + "\n".join(lines)
        )

    return get_maintenance_history


def get_available_technicians() -> str:
    """Get the list of technicians who are currently available."""

    techs = Technician.objects.filter(is_available=True)

    if not techs.exists():
        return "No technicians are currently available."

    return "Available technicians:\n" + "\n".join(
        f"- {t.user.username} (Specialty: {t.specialty})"
        for t in techs
    )



def make_book_appointment_tool(user):
    def book_appointment(
        license_plate: str,
        scheduled_date: str,
        notes: str = ""
    ) -> str:

        # Find the vehicle
        try:
            vehicle = Vehicle.objects.get(
                license_plate__iexact=license_plate
            )
        except Vehicle.DoesNotExist:
            return f"No vehicle found with license plate {license_plate}."

        # Permission check
        if user.role == user.Role.CUSTOMER and vehicle.owner_id != user.id:
            return "You are not authorized to book an appointment for this vehicle."

        # Parse date and time
        dt = parse_datetime(scheduled_date)

        if dt is None:
            return (
                "Could not understand that date/time. "
                "Please use the format YYYY-MM-DD HH:MM."
            )

        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)

        # Allowed service times
        allowed_times = [
            "09:00",
            "11:00",
            "13:00",
            "15:00",
        ]

        requested_time = dt.strftime("%H:%M")

        if requested_time not in allowed_times:
            return (
                "This is not a valid service slot. "
                "Available times are 09:00, 11:00, 13:00, and 15:00."
            )

        # Prevent booking in the past
        if dt <= timezone.now():
            return "You cannot book an appointment in the past."

        # Find an available technician
        technicians = Technician.objects.filter(is_available=True)

        if not technicians.exists():
            return "No technicians are currently available."

        selected_technician = None

        for technician in technicians:
            already_booked = Appointment.objects.filter(
                technician=technician,
                scheduled_date=dt,
                status__in=[
                    Appointment.Status.PENDING,
                    Appointment.Status.CONFIRMED,
                ],
            ).exists()

            if not already_booked:
                selected_technician = technician
                break

        if selected_technician is None:
            return (
                "This service slot is already fully booked. "
                "Please choose another available slot."
            )

        # Create appointment
        appointment = Appointment.objects.create(
            vehicle=vehicle,
            technician=selected_technician,
            scheduled_date=dt,
            notes=notes,
        )

        return (
            f"Appointment booked successfully for {vehicle} "
            f"with technician {selected_technician.user.username} "
            f"on {appointment.scheduled_date}. "
            f"Status: {appointment.status}."
        )

    return book_appointment




def make_cancel_appointment_tool(user):
    """Creates a cancellation tool that knows which user is making the request."""

    def cancel_appointment(
        license_plate: str,
        scheduled_date: str
    ) -> str:
        """Cancel an existing pending appointment."""

        try:
            vehicle = Vehicle.objects.get(
                license_plate__iexact=license_plate
            )
        except Vehicle.DoesNotExist:
            return f"No vehicle found with license plate {license_plate}."

        if (
            user.role == user.Role.CUSTOMER
            and vehicle.owner_id != user.id
        ):
            return (
                "You are not authorized to cancel appointments "
                "for this vehicle."
            )

        dt = parse_datetime(scheduled_date)

        if dt is None:
            return (
                "Could not understand that date/time. "
                "Please use the format YYYY-MM-DD HH:MM."
            )

        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)

        appointment = Appointment.objects.filter(
            vehicle=vehicle,
            scheduled_date=dt,
            status=Appointment.Status.PENDING,
        ).first()

        if not appointment:
            return (
                "No matching pending appointment found "
                "for that date and time."
            )

        appointment.status = Appointment.Status.CANCELLED
        appointment.save()

        return (
            f"Appointment for {vehicle} on "
            f"{appointment.scheduled_date} has been cancelled."
        )

    return cancel_appointment



def get_available_service_slots() -> str:
    """Get available service appointment slots."""

    technicians = Technician.objects.filter(is_available=True)

    if not technicians.exists():
        return "No technicians are currently available."

    now = timezone.now()

    # Fixed service slots for each day
    slot_times = [
        "09:00",
        "11:00",
        "13:00",
        "15:00",
    ]

    available_slots = []

    for day_offset in range(7):
        date = (now + timezone.timedelta(days=day_offset)).date()

        for time in slot_times:
            slot_datetime = timezone.make_aware(
                timezone.datetime.combine(
                    date,
                    timezone.datetime.strptime(time, "%H:%M").time()
                )
            )

            for technician in technicians:

                already_booked = Appointment.objects.filter(
                    technician=technician,
                    scheduled_date=slot_datetime,
                    status__in=[
                        Appointment.Status.PENDING,
                        Appointment.Status.CONFIRMED,
                    ],
                ).exists()

                if not already_booked:
                    available_slots.append(
                        f"- {date} at {time} "
                        f"| Technician: {technician.user.username} "
                        f"| Specialty: {technician.specialty}"
                    )

    if not available_slots:
        return "No available service slots were found in the next 7 days."

    return (
        "Available service slots for the next 7 days:\n"
        + "\n".join(available_slots)
    )




def make_get_due_services_tool(user):
    """Get vehicles that are due or overdue for maintenance."""

    def get_due_services() -> str:

        if user.role == user.Role.CUSTOMER:
            vehicles = Vehicle.objects.filter(owner=user)
        else:
            vehicles = Vehicle.objects.all()

        today = timezone.localdate()

        due_services = []

        for vehicle in vehicles:

            last_record = vehicle.maintenance_records.order_by(
                '-service_date'
            ).first()

            if not last_record or not last_record.next_service_date:
                continue

            if last_record.next_service_date < today:
                status = 'Overdue'

            elif last_record.next_service_date <= today + timezone.timedelta(days=7):
                status = 'Due Soon'

            else:
                continue

            due_services.append(
                f"- {vehicle.make} {vehicle.model} "
                f"({vehicle.license_plate}) | "
                f"Next service: {last_record.next_service_date} | "
                f"Status: {status}"
            )

        if not due_services:
            return "No vehicles currently need maintenance."

        return (
            "Vehicles that need maintenance:\n"
            + "\n".join(due_services)
        )

    return get_due_services

