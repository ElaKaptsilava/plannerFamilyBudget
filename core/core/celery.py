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
            "schedule": crontab(minute=0, hour=2),
            "options": {
                "queue": "default",
            },
        },
        "update_monthly_incomes": {
            "task": "budgets_manager.tasks.update_monthly_incomes",
            "schedule": crontab(hour=23, minute=50, day_of_month=last_day_of_month),
            "options": {
                "queue": "default",
            },
        },
    },
    timezone="UTC",
)
