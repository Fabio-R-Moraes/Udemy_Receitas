from django.apps import AppConfig


class ReceitasappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'receitasApp'

    def ready(self, *args, **kwargs) -> None:
        import receitasApp.signals #noqa
        super_ready = super().ready(*args, **kwargs)

        return super_ready
