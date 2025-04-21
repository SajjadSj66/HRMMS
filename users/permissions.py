from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUserOrReadOnly(BasePermission):
    """
    Only admins have the right to create, edit, and delete. Everyone else has read-only rights.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin'


class IsAuthenticatedAndOwner(BasePermission):
    """
    Only the user can change their own information or password.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user or getattr(request.user, 'role', None) == 'admin'
