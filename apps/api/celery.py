import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.settings")

app = Celery("apps")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-price-for-unprocessed-packages': {
        'task': 'api.tasks.calculate_delivery_prices',
        'schedule': 60*5,  # every 5 minutes
    },
}
