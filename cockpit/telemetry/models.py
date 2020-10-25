import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class CockpitUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Sensor(models.Model):
    TYPE_CHOICES = (
        ("TEMPERATURE", "Temperature"),
        ("SPEED", "Speed"),
        ("ROTATION", "Rotation"),
        ("FLUID_LEVEL", "Fluid Level"),
        ("FLUID_PRESSURE", "Fluid Pressure"),
        ("VOLTAGE", "Voltage"),
        ("AMPERAGE", "Amerage"),
        ("WATT", "Wattage"),
        ("POSITION", "Position")
    )
    UNIT_CHOICES = (
        ("C", "Celsius"),
        ("KPH", "Kilometers per Hour"),
        ("RPM", "Rotations per Minute"),
        ("MM", "Millimeters"),
        ("BAR", "Bars"),
        ("V", "Volts"),
        ("A", "Amps"),
        ("AH", "Amp Hours"),
        ("W", "Watts"),
        ("LON", "Longitude"),
        ("LAT", "Latitude"),
    )
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40)
    category = models.CharField(max_length=20, choices=TYPE_CHOICES)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CockpitUser, related_name='sensor_created_by_user',
        on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        CockpitUser, related_name='sensor_updated_by_user',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}, {self.category}, {self.unit}"


class Machine(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40)
    sensors = models.ManyToManyField(Sensor)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CockpitUser, related_name='machine_created_by_user',
        on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        CockpitUser, related_name='machine_updated_by_user',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"{self.name}"
        )


class TelemetryEntry(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    machine = models.ForeignKey(
        Machine, on_delete=models.CASCADE,
        related_name="machine_telemetry_entry"
    )
    sensor = models.ForeignKey(
        Sensor, on_delete=models.CASCADE,
        related_name="sensor_telemetry_entry"
    )
    value = models.DecimalField(max_digits=12, decimal_places=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CockpitUser, related_name='telemetry_entry_created_by_user',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"{self.machine}, {self.sensor}, {self.value}, "
            f"{self.created_at}"
        )
