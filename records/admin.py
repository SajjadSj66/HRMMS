from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "record_date", "diagnosis")
    search_fields = ("patient__username", "doctor__username", "diagnosis", "treatment")
    list_filter = ("record_date", "doctor")
    ordering = ("-record_date",)
    readonly_fields = ("record_date", "doctor")

    def get_queryset(self, request):
        """Restrict non-superusers from seeing all records."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(doctor=request.user) if request.user.is_staff else qs.filter(patient=request.user)

    def has_add_permission(self, request):
        """Only allow doctors to add medical records."""
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        """Only allow doctors to modify medical records."""
        if obj is None:
            return True
        return obj.doctor == request.user

    def has_delete_permission(self, request, obj=None):
        """Only allow doctors to delete their own records."""
        if obj is None:
            return True
        return obj.doctor == request.user


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ("test_name", "patient", "doctor", "test_date")
    search_fields = ("test_name", "patient__username", "doctor__username")
    list_filter = ("test_name",)
