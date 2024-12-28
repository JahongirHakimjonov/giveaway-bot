import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "every-2-hour-task": {
        "task": "apps.support.tasks.check.check_users_in_groups",
        "schedule": crontab(minute=0, hour="*/2"),
    },
}

app.autodiscover_tasks()
