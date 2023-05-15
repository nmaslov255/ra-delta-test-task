from django.core.cache import cache
from celery.utils.log import get_task_logger
from requests.exceptions import HTTPError

from .celery import app
from .utils import fetch_rub_exchange_rate


logger = get_task_logger(__name__)

@app.task(bind=True, autoretry_for=(HTTPError,),
          retry_kwargs={'max_retries': 5})
def fetch_rub_to_usd_exchange_rate(self):
    """Celery task that cached USD exchange rate
    """
    try:
        rub_usd_pair_price = fetch_rub_exchange_rate('USD')
        cache.set('rub_usd_pair_price', rub_usd_pair_price)
        logger.info(f'Cached rub_usd_pair_price={rub_usd_pair_price}')
    except HTTPError as e:
        logger.error('HTTPError when try to fetch usd exchange rate')
        self.retry(exc=e, countdown=60*5)
    except Exception as e:
        logger.error(
            f'Unexpected exception when try to fetch usd exchange rate: {e}'
        )
