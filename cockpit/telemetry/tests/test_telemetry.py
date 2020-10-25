import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from cockpit.telemetry.models import (CockpitUser, Machine, Sensor,
                                      TelemetryEntry)
from cockpit.telemetry.schema import schema
from django.db.models.signals import post_save
from django.test import TestCase
from graphene.test import Client
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer
from graphene_subscriptions.signals import post_save_subscription
from mixer.backend.django import mixer

sensor_list = """
    query
    {
        allSensors
        {
            id
            name
            unit
            createdAt
        }
    }
"""

machine_list = """
    query
    {
        allMachines
        {
            id
            name
            sensors
            {
                id
                name
                unit
                createdAt
            }
            createdAt
        }
    }
"""

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
class TestSensorSchema(TestCase):

    def setUp(self):
        self.client = Client(schema)

    def test_sensor_list_query(self):
        for n in range(50):
            mixer.blend(Sensor)
        response = self.client.execute(
            sensor_list
        )
        response_sensors = response.get("data").get(
            "allSensors")
        assert len(response_sensors) == 50


@pytest.mark.django_db
class TestMachineSchema(TestCase):

    def setUp(self):
        self.client = Client(schema)

    def test_sensor_list_query(self):
        for n in range(50):
            machine = mixer.blend(Machine)
            for n in range(5):
                sensor = mixer.blend(Sensor)
                machine.sensors.add(sensor)
            machine.save()

        response = self.client.execute(
            machine_list
        )
        response_sensors = response.get("data").get(
            "allMachines")
        assert len(response_sensors) == 50


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

    def test_telemetry_entry_list_query(self):
        for n in range(50):
            mixer.blend(TelemetryEntry)
        response = self.client.execute(
            telemetry_entry_list
        )
        response_telemetry_entries_list = response.get("data").get(
            "allTelemetryEntries")
        assert len(response_telemetry_entries_list) == 50


async def query(query, communicator, variables=None):
    await communicator.send_json_to(
        {"id": 1, "type": "start", "payload": {
            "query": query, "variables": variables}}
    )


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_model_created_subscription_succeeds():
    post_save.connect(
        post_save_subscription, sender=TelemetryEntry,
        dispatch_uid="current_temperature_subscribe_test"
    )

    communicator = WebsocketCommunicator(
        GraphqlSubscriptionConsumer, "/graphql/")
    connected, subprotocol = await communicator.connect()
    assert connected

    subscription = """
        subscription {
            currentTemperatureSubscribe {
                temperature {
                    value
                }
            }
        }
    """

    await query(subscription, communicator)
    user = await sync_to_async(CockpitUser.objects.create)(
        username="test"
    )
    machine = await sync_to_async(Machine.objects.create)(
        name="test", created_by=user, updated_by=user
    )
    sensor = await sync_to_async(Sensor.objects.create)(
        name="test", category="TEMPERATURE", unit="C",
        created_by=user, updated_by=user
    )
    telemetry_entry = await sync_to_async(TelemetryEntry.objects.create)(
        machine=machine, sensor=sensor, created_by=user,
        value="42.314"
    )

    response = await communicator.receive_json_from()
    assert response["payload"]["data"][
        "currentTemperatureSubscribe"][
            "temperature"]["value"] == telemetry_entry.value

    post_save.disconnect(
        post_save_subscription, sender=TelemetryEntry,
        dispatch_uid="current_temperature_subscribe_test"
    )
