from django.apps import AppConfig


class RecipientAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recipient_app"

    def ready(self):
        import recipient_app.signals
