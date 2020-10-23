import os

import channels_graphql_ws
import django
from asgiref.compatibility import guarantee_single_callable
from channels.routing import ProtocolTypeRouter, URLRouter
from cockpit.telemetry.schema import schema
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cockpit.settings')

class GraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""
    schema = schema

    # Uncomment to send keepalive message every 42 seconds.
    # send_keepalive_every = 42

    # Uncomment to process requests sequentially (useful for tests).
    # strict_ordering = True

    async def on_connect(self, payload):
        """New client connection handler."""
        # You can `raise` from here to reject the connection.
        print("New client connected!")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': URLRouter([
        django.urls.path('graphql/', GraphqlWsConsumer),
    ])
})
