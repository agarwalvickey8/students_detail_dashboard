from django.apps import AppConfig


class StaffsignupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'staffsignup'


    def ready(self):
        import staffsignup.signals