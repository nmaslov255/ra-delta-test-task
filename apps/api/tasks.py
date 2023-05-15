from celery.utils.log import get_task_logger
from django.db.models import F
from django.core.cache import cache

from .celery import app
from .models import Package
from .utils import fetch_rub_exchange_rate


logger = get_task_logger(__name__)


@app.task
def calculate_delivery_prices():
    """Celery task that update deliver_price for unprocessed packages"""
    usd_rub_pair = cache.get('usd_rub_pair')

    if not usd_rub_pair:
        usd_rub_pair = fetch_rub_exchange_rate('USD')
        cache.set('usd_rub_pair', usd_rub_pair)

    rows_updated = Package.objects.filter(delivery_price=None).update(
        delivery_price=(F('weight')*0.5*F('price')*0.01)*usd_rub_pair
    )

    logger.info(f'Succesfully updated {rows_updated} package rows')
