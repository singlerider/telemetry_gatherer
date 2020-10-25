import json

import graphene
from cockpit.telemetry.models import Machine, Sensor, TelemetryEntry
from graphene_django import DjangoObjectType
from graphene_django.types import DjangoObjectType
from graphene_subscriptions.events import CREATED


class SensorType(DjangoObjectType):
    class Meta:
        model = Sensor
        fields = (
            "id", "name", "category", "unit",
            "created_at", "updated_at", "created_by", "updated_by"
        )


class MachineType(DjangoObjectType):
    class Meta:
        model = Machine
        fields = (
            "id", "name", "sensors",
            "created_at", "updated_at", "created_by", "updated_by"
        )


class TelemetryEntryType(DjangoObjectType):
    class Meta:
        model = TelemetryEntry
        fields = (
            "id", "machine", "sensor", "value",
            "created_at", "updated_at", "created_by"
        )


class CurrentTemperatureType(DjangoObjectType):
    class Meta:
        model = TelemetryEntry
        fields = ("id", "value")

    timestamp = graphene.DateTime()
    unit = graphene.String()
    value = graphene.Decimal()


class Query(graphene.ObjectType):
    all_sensors = graphene.List(SensorType)
    all_machines = graphene.List(MachineType)
    all_telemetry_entries = graphene.List(TelemetryEntryType)
    current_temperature = graphene.Field(CurrentTemperatureType)

    def resolve_all_sensors(self, info):
        return Sensor.objects.all().order_by("-created_at")

    def resolve_all_machines(self, info):
        return Machine.objects.all().order_by("-created_at")

    def resolve_all_telemetry_entries(self, info):
        return TelemetryEntry.objects.all().order_by("-created_at")

    def resolve_current_temperature(self, info):
        latest_entry = TelemetryEntry.objects.filter(
            sensor__category="TEMPERATURE",
            sensor__unit="C"
        ).latest('created_at')
        latest_entry.timestamp = latest_entry.created_at
        latest_entry.unit = latest_entry.sensor.unit
        return latest_entry
        
        
class Subscription(graphene.ObjectType):
    current_temperature_subscribe = graphene.Field(CurrentTemperatureType)

    def resolve_current_temperature_subscribe(root, info):
        return root.filter(
            lambda event:
                event.operation == CREATED and
                isinstance(event.instance, TelemetryEntry)
        ).map(lambda event: event.instance)


schema = graphene.Schema(query=Query, subscription=Subscription)
