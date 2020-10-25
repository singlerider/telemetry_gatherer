from cockpit.telemetry.models import TelemetryEntry
from django.db.models.signals import post_save
from graphene_subscriptions.signals import post_save_subscription

post_save.connect(post_save_subscription, sender=TelemetryEntry,
                  dispatch_uid="current_temperature_subscribe")
