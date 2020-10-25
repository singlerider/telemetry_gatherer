from django.db.models.signals import post_save, post_delete
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription

from cockpit.telemetry.models import TelemetryEntry

post_save.connect(post_save_subscription, sender=TelemetryEntry, dispatch_uid="current_temperature_subscribe")
