import json

import graphene
from cockpit.telemetry.models import Machine, Sensor, TelemetryEntry
from graphene_django import DjangoObjectType
import channels_graphql_ws


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


class TelemetrySubscription(channels_graphql_ws.Subscription):
    """Simple GraphQL subscription."""

    # Subscription payload.
    event = graphene.String()

    class Arguments:
        """That is how subscription arguments are defined."""
        arg1 = graphene.String()
        arg2 = graphene.String()

    @staticmethod
    def subscribe(root, info, arg1, arg2):
        """Called when user subscribes."""

        # Return the list of subscription group names.
        return ['group42']

    @staticmethod
    def publish(payload, info, arg1, arg2):
        """Called to notify the client."""

        # Here `payload` contains the `payload` from the `broadcast()`
        # invocation (see below). You can return `MySubscription.SKIP`
        # if you wish to suppress the notification to a particular
        # client. For example, this allows to avoid notifications for
        # the actions made by this particular client.

        return TelemetrySubscription(event='Something has happened!')
        

class Subscription(graphene.ObjectType):
    """Root GraphQL subscription."""
    telemetry_subscription = TelemetrySubscription.Field()


schema = graphene.Schema(query=Query, subscription=Subscription)
