from rest_framework.permissions import BasePermission

class AppointmentPermission(BasePermission):
    """
    Permission rules:
    - POST: Only patients can create appointments.
    - PUT: Only doctors or nurses can update appointments.
    - DELETE: Only doctors or patients can delete appointments.
    - GET: Any authenticated user can view.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return hasattr(request.user, 'patient')
        elif request.method == 'PUT':
            return hasattr(request.user, 'doctor') or hasattr(request.user, 'nurse')
        elif request.method == 'DELETE':
            return hasattr(request.user, 'doctor') or hasattr(request.user, 'patient')
        return True  # Allow GET or other methods if needed
