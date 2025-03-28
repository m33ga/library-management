from django.apps import AppConfig


class MemberAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "member_auth"

    def ready(self):
        import member_auth.signals