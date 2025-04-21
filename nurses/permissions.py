from rest_framework import permissions
from .models import Nurse

class IsStaffOrOwnNurseProfile(permissions.BasePermission):
    """
    Allows admins to see all profiles,
    And regular users to see only their own nursing profile.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user
