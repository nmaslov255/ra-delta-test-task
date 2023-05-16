import logging
from rest_framework import permissions


logger = logging.getLogger('apps.api')


class IsSessionOwner(permissions.BasePermission):
    """
    Allow access for object only for session owner.
    """

    def has_object_permission(self, request, view, obj):
        client_session = request.session.session_key
        object_session = str(obj.owner_session)

        if client_session != object_session:
            ip = request.META.get("REMOTE_ADDR")
            path = request.META.get("PATH_INFO")

            message = (
                f'"{request.method} {path}" Client requested resource '
                f'without permissions (session={client_session}, ip={ip})'
            )

            logger.error(message)

            return False
        return True
