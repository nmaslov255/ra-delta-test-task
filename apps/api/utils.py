import requests

from .exceptions import CurrencyNotFound
from .validators import raise_for_invalide_cbr_json


def fetch_rub_exchange_rate(target_ticker: str) -> float:
    """Return value of the target currency in rubles

    Args:
        target_ticker (str): Currency ticker like USD, GBP, etc...

    Returns:
        float: Value of targer currency ticker

    Raises:
        HTTPError: Error status code in http(s) response
        ValidationError: JSON response is invalide
        CurrencyNotFound: No targer ticker in json response
    """
    response = requests.get(
        'https://www.cbr-xml-daily.ru/daily_json.js',
        timeout=60
    )

    if response.status_code != 200:
        response.raise_for_status()
    response = response.json()

    raise_for_invalide_cbr_json(response)
    currency = response.get('Valute').get(target_ticker)

    if not currency:
        raise CurrencyNotFound(target_ticker)
    return currency.get('Value')
