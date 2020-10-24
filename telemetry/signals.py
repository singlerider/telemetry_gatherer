from django.db.models.signals import post_save, post_delete
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription

from .models import Sensor

# you have to connect your model to django singals

# this django siganl is triggered when an entry is saved to your model 
post_save.connect(post_save_subscription, sender=Sensor, dispatch_uid="SensorSubscription")

# this django signal is trigerred when an entry is deleted from your model
post_delete.connect(post_delete_subscription, sender=Sensor, dispatch_uid="SensorSubscription")

