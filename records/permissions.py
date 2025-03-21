from rest_framework import permissions

class IsDoctorOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "doctor":
            return obj.doctor == request.user
        if request.user.role == "patient":
            return obj.patient == request.user
        return False
