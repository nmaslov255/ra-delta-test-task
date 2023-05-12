from rest_framework.exceptions import APIException


class SessionNotCreated(APIException):
    status_code = 511
    default_detail = 'Session not created'
