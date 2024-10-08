import calendar
import os

from celery import Celery
from celery.schedules import crontab
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()

last_day_of_month = calendar.monthrange(timezone.now().year, timezone.now().month)[1]

app.conf.update(
    beat_schedule={
        "update_target_deadlines": {
            "task": "targets.tasks.update_target_deadlines",
            "schedule": crontab(minute=0, hour=0),
            "options": {
                "queue": "default",
            },
        },
        "update_subscription_status": {
            "task": "subscriptions.tasks.update_subscription_status",
            "schedule": crontab(minute=0, hour=0),
            "options": {
                "queue": "default",
            },
        },
        "generate_next_subscription": {
            "task": "subscriptions.tasks.generate_next_subscription",
            "schedule": crontab(minute=0, hour=0),
            "options": {
                "queue": "default",
            },
        },
        "update_monthly_incomes": {
            "task": "budgets_manager.tasks.update_monthly_incomes",
            "schedule": crontab(hour=0, minute=0, day_of_month=last_day_of_month),
            "options": {
                "queue": "default",
            },
        },
        "generate_budget_analysis_message": {
            "task": "budgets_manager.tasks.generate_budget_analysis_message",
            "schedule": crontab(minute=0, hour=0, day_of_week=1),
            "options": {
                "queue": "default",
            },
        },
    },
    timezone="UTC",
)
