import json

import graphene
from .models import Machine, Sensor, TelemetryEntry
from graphene_django import DjangoObjectType


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
        return Sensor.objects.all()

    def resolve_all_machines(self, info):
        return Machine.objects.all()

    def resolve_all_telemetry_entries(self, info):
        return TelemetryEntry.objects.all()

    def resolve_current_temperature(self, info):
        latest_entry = TelemetryEntry.objects.filter(
            sensor__category="TEMPERATURE",
            sensor__unit="C"
        ).last()
        latest_entry.timestamp = latest_entry.created_at
        latest_entry.unit = latest_entry.sensor.unit
        return latest_entry


import graphene
from rx import Observable

class Subscription(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return Observable.interval(3000) \
                         .map(lambda i: "hello world!")


schema = graphene.Schema(query=Query, subscription=Subscription)
