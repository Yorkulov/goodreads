from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):   # signals ishlashi uchun kk ishlamadi bug == comment
        import users.signals
