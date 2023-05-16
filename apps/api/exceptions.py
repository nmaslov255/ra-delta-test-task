from rest_framework.exceptions import APIException
from apps.settings import MAX_USD_RUB_EXCHANGE_RATE


class SessionNotCreated(APIException):
    status_code = 511
    default_detail = 'Session not created'


class CurrencyNotFound(Exception):
    def __init__(self, ticker):
        super().__init__(f"{ticker} not found in json responce")


class USDExchangeRateIsTooHigh(Exception):
    def __init__(self, value):
        error_msg = (
             "The USD/RUB exchange rate is higher then "
            f"maximum rate ({value} > {MAX_USD_RUB_EXCHANGE_RATE})"
        )
        super().__init__(error_msg)
