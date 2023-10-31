from django.apps import AppConfig


class SkillfactoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "moykotel"

    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов