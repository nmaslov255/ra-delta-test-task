from celery.utils.log import get_task_logger

from .celery import app


logger = get_task_logger(__name__)


@app.task
def fetch_rub_to_usd_exchange_rate():
    logger.info("Try to fetch RUB/USD exchange rate")
