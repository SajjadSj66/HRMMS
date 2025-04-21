from rest_framework import permissions


class IsDoctor(permissions.BasePermission):
    """
    Only users with the role 'doctor' are allowed to submit prescriptions.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return hasattr(request.user, 'role') and request.user.role == "doctor"
        return True


class IsPatient(permissions.BasePermission):
    """
    Allow access only to users whose role is 'patient'.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) == "patient"
