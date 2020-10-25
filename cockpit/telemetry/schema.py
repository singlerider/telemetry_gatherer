import json

import graphene
from cockpit.telemetry.models import Machine, Sensor, TelemetryEntry
from graphene_django import DjangoObjectType
from graphene_django.types import DjangoObjectType
from graphene_subscriptions.events import CREATED
from graphene_subscriptions.subscriptions import DjangoObjectSubscription


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


class CreateTelemetryEntry(graphene.Mutation):
    class Arguments:
        machine_id = graphene.ID(required=True)
        sensor_id = graphene.ID(required=True)
        value = graphene.Decimal(required=True)

    telemetry_entry = graphene.Field(lambda: TelemetryEntryType)

    def mutate(self, info, machine_id, sensor_id, value):
        machine = Machine.objects.get(pk=machine_id)
        sensor = Sensor.objects.get(pk=sensor_id)
        telemetry_entry = TelemetryEntry(
            machine=machine,
            sensor=sensor,
            value=value
        )
        return CreateTelemetryEntry(telemetry_entry=telemetry_entry)


class CurrentTemperatureSubscription(DjangoObjectSubscription):
    class Meta:
        model = TelemetryEntry
        output = CurrentTemperatureType

    class Arguments:
        pass

    def subscribe(root, info, operation, instance, *args, **kwargs):
        import pdb; pdb.set_trace()
        if operation == "created":
            import pdb; pdb.set_trace()


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


class Mutation(graphene.ObjectType):
    create_telemetry_entry = CreateTelemetryEntry.Field()
        
        
class Subscriptions(graphene.ObjectType):
    current_temperature_subscribe = CurrentTemperatureSubscription.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscriptions)
