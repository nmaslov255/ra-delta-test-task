from rest_framework import permissions


class IsSessionOwner(permissions.BasePermission):
    """
    Allow access for object only for session owner.
    """

    def has_object_permission(self, request, view, obj):
        try:
            return str(obj.owner_session) == request.session.session_key
        except AttributeError:
            # TODO: add logs errro
            return False
