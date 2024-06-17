import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()

app.conf.update(
    beat_schedule={
        "update-target-deadlines": {
            "task": "targets.tasks.update_target_deadlines",
            "schedule": crontab(minute=0, hour=2),
            "options": {
                "queue": "default",
            },
        },
    },
    timezone="UTC",
)
