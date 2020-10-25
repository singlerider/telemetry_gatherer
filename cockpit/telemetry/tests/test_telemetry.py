import pytest
from cockpit.telemetry.models import (CockpitUser, Machine, Sensor,
                                      TelemetryEntry)
from cockpit.telemetry.schema import schema
from django.test import TestCase
from graphene.test import Client
from mixer.backend.django import mixer

telemetry_entry_list = """
    query
    {
        allTelemetryEntries
        {
            id
            value
            sensor {
                id
                name
                unit
                createdAt
            }
            machine {
                id
                name
                createdAt
            }
        }
    }
"""

current_temperature_entry = """
    query
    {
        currentTemperature
        {
            id
            timestamp
            value
            unit
        }
    }
"""


@pytest.mark.django_db
class TestTelemetryEntrySchema(TestCase):

    def setUp(self):
        self.client = Client(schema)

    def test_current_temperature_entry_query(self):
        user = mixer.blend(CockpitUser)
        machine = mixer.blend(Machine)
        sensor = mixer.blend(Sensor)
        sensor.category = "TEMPERATURE"
        sensor.unit = "C"
        sensor.save()
        machine.sensors.add(sensor)
        machine.save()
        telemetry_entry = TelemetryEntry(
            machine=machine, sensor=sensor,
            value="-60.00",
            created_by=user
        )
        telemetry_entry.save()
        response = self.client.execute(
            current_temperature_entry
        )
        response_current_temperature = response.get(
            "data").get("currentTemperature")
        assert response_current_temperature["id"] == str(
            telemetry_entry.id)
