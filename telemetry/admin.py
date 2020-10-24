from django.contrib import admin

from .models import Machine, Sensor, TelemetryEntry

admin.site.register(Sensor)
admin.site.register(Machine)
admin.site.register(TelemetryEntry)
