from rest_framework.permissions import BasePermission

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        user = request.user
        method = request.method
        if (method in SAFE_METHODS or user and user.is_authenticated and user.is_superuser):
            return True
        return False
