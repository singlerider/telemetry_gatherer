import graphene
from cockpit.telemetry.models import (CockpitUser, Machine, Sensor,
                                      TelemetryEntry)
from graphene import ObjectType
from graphene_django import DjangoObjectType
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


class TemperatureType(DjangoObjectType):
    class Meta:
        model = TelemetryEntry
        fields = ("id", "value")

    timestamp = graphene.DateTime()
    unit = graphene.String()
    value = graphene.Decimal()


class TemperatureSubscribeType(ObjectType):
    temperature = graphene.Field(TemperatureType)


class CreateTelemetryEntry(graphene.Mutation):
    class Arguments:
        machine_id = graphene.ID(required=True)
        sensor_id = graphene.ID(required=True)
        value = graphene.Decimal(required=True)
        created_by_id = graphene.ID(required=True)

    telemetry_entry = graphene.Field(lambda: TelemetryEntryType)
    timestamp = graphene.DateTime()
    unit = graphene.String()

    def mutate(self, info, machine_id, sensor_id, value, created_by_id):
        machine = Machine.objects.get(pk=machine_id)
        sensor = Sensor.objects.get(pk=sensor_id)
        user = CockpitUser.objects.get(pk=created_by_id)
        telemetry_entry = TelemetryEntry(
            machine=machine,
            sensor=sensor,
            value=value,
            created_by=user
        )
        telemetry_entry.timestamp = telemetry_entry.created_at
        telemetry_entry.unit = telemetry_entry.sensor.unit
        telemetry_entry.save()
        return CreateTelemetryEntry(telemetry_entry=telemetry_entry)


class Query(graphene.ObjectType):
    all_sensors = graphene.List(SensorType)
    all_machines = graphene.List(MachineType)
    all_telemetry_entries = graphene.List(TelemetryEntryType)
    current_temperature = graphene.Field(TemperatureType)

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
        ).latest("-created_at")
        latest_entry.timestamp = latest_entry.created_at
        latest_entry.unit = latest_entry.sensor.unit
        return latest_entry


class Mutation(graphene.ObjectType):
    create_telemetry_entry = CreateTelemetryEntry.Field()


class Subscription(graphene.ObjectType):
    current_temperature_subscribe = graphene.Field(TemperatureSubscribeType)

    def resolve_current_temperature_subscribe(root, info):
        def build_response(event):
            event.instance.temperature = TelemetryEntry()
            event.instance.temperature.value = event.instance.value
            event.instance.temperature.timestamp = event.instance.created_at
            event.instance.temperature.unit = event.instance.sensor.unit
            return event.instance

        return root.filter(
            lambda event:
                event.operation == CREATED and
                isinstance(event.instance, TelemetryEntry)
        ).map(lambda event: build_response(event))


schema = graphene.Schema(query=Query, mutation=Mutation,
                         subscription=Subscription)
