from django.apps import AppConfig


class TelemetryConfig(AppConfig):
    name = 'cockpit.telemetry'

    def ready(self):
        import cockpit.telemetry.signals
