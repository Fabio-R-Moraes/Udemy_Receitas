from django.apps import AppConfig

class AutoresappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autoresApp'

    def ready(self, *args, **kwargs) -> None:
        import autoresApp.signals #noqa
        super_ready = super().ready(*args, **kwargs)

        return super_ready
