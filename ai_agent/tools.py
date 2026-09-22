from vehicles.models import Vehicle, Technician


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