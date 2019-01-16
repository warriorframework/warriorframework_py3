from rest_framework.permissions import BasePermission
"""
This module defines add-ons for Django Rest Framework regarding users,
such as new authentication classes, permission classes, views, and decorators.
"""


class IsNotExpiredPermission(BasePermission):
    message = 'User is expired'

    def has_permission(self, request, view):
        user = request.user
        try:
            return not user.expired()
        except AttributeError:
            pass
        return False
