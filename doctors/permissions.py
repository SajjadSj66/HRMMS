from rest_framework.permissions import BasePermission
from .models import Doctor
class IsDoctorOrCreateOnly(BasePermission):
    """
    - Only doctors can GET (show their information)
    - Only users without a doctor profile can POST (create a profile)
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return Doctor.objects.filter(user=request.user).exists()
