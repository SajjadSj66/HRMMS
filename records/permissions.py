from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    """Only doctors are allowed."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) == "doctor"


class IsOwnerDoctorOfRecord(BasePermission):
    """Only the doctor who created the record has permission to edit or view it."""
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and hasattr(request.user, "doctor") and obj.doctor == request.user.doctor


class IsDoctorOrAdminForDelete(BasePermission):
    """Only the doctor who owns the record or the admin can delete it."""
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if getattr(user, "role", None) == "admin":
            return True
        if getattr(user, "role", None) == "doctor" and hasattr(user, "doctor"):
            return obj.doctor == user.doctor
        return False


class IsDoctorOrPatient(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.doctor or request.user == obj.patient


class IsDoctorAndOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.doctor