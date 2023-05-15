from rest_framework.exceptions import APIException


class SessionNotCreated(APIException):
    status_code = 511
    default_detail = 'Session not created'


class CurrencyNotFound(Exception):
    def __init__(self, ticker):
        super().__init__(f"{ticker} not found in json responce")
