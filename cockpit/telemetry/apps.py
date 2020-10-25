from django.apps import AppConfig


class TelemetryConfig(AppConfig):
    name = 'telemetry'

    def ready(self):
        import cockpit.telemetry.signals
