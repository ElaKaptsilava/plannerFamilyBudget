from django.apps import AppConfig


class BudgetsManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "budgets_manager"

    def ready(self):
        import budgets_manager.signals  # noqa: F401
