from rest_framework import permissions
from .models import Patient

class IsOwnerOrAdminCanDelete(permissions.BasePermission):
    """
    Only the patient owner (for GET, PUT, PATCH) or admin (for DELETE) is allowed.
    """

    def has_permission(self, request, view):
        """All authenticated users are allowed to POST."""
        if request.method == 'POST':
            return request.user and request.user.is_authenticated

        """Must be admin to DELETE"""
        if request.method == 'DELETE':
            return request.user.is_staff

        return True

    def has_object_permission(self, request, view, obj):
        """Only the profile owner can GET/PUT/PATCH."""
        if request.method in ['GET', 'PUT', 'PATCH']:
            return obj.user == request.user

        """DELETE only by admin"""
        if request.method == 'DELETE':
            return request.user.is_staff

        return False
