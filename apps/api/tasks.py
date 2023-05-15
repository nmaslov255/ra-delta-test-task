from celery.utils.log import get_task_logger
from django.db.models import F
from django.core.cache import cache

from .celery import app
from .models import Package
from .utils import (
    get_rub_exchange_rate_or_none,
    fetch_rub_exchange_rate
)


logger = get_task_logger(__name__)


@app.task(bind=True, retry_kwargs={'max_retries': 5})
def fetch_rub_to_usd_exchange_rate(self):
    """Celery task that cached USD exchange rate"""
    usd_rub_pair = get_rub_exchange_rate_or_none('USD')

    if not usd_rub_pair:
        logger.error("Can't get exchange pair, retrying later")
        self.retry(countdown=60*5)

    cache.set('usd_rub_pair', usd_rub_pair)

@app.task
def calculate_delivery_prices():
    """Celery task that update deliver_price for unprocessed packages"""
    usd_rub_pair = cache.get('usd_rub_pair')

    if not usd_rub_pair:
        usd_rub_pair = fetch_rub_exchange_rate('USD')
        cache.set('usd_rub_pair', usd_rub_pair)

    Package.objects.filter(delivery_price=None).update(
        delivery_price=(F('weight')*0.5*F('price')*0.01)*usd_rub_pair
    )
