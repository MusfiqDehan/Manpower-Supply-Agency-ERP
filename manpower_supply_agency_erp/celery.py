# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "manpower_supply_agency_erp.settings.production"
)

app = Celery("manpower_supply_agency_erp")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Add the broker_connection_retry_on_startup setting
app.conf.broker_connection_retry_on_startup = True


app.conf.beat_schedule = {
    "run-create-notification": {
        "task": "dashboard_app.tasks.run_create_notification",
        "schedule": crontab(
            hour=0, minute=0, day_of_month="1"
        ),  # Runs on the first day of every month at midnight
        # "schedule": crontab(
        #     hour=0, minute=0, day_of_week="monday"
        # ),  # Runs every Sunday at midnight
        # "schedule": crontab(hour=0, minute=0),  # Runs every day at midnight
        # "schedule": crontab(minute="*"),  # Runs every minute
    },
}
