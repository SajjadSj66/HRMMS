from django.contrib import admin
from .models import Prescription


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("patient_id", "prescriber", "medical_details", "issued_date")
    list_filter = ("issued_date", "prescriber")
    search_fields = ("patient__username", "prescribed_by__username", "medical_details")
    readonly_fields = ("issued_date", "prescriber")

    def save_model(self, request, obj, form, change):
        """Ensure that only doctors can assign prescriptions and set prescribed_by."""
        if not obj.pk:  # If it's a new object
            obj.prescribed_by = request.user


class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = ("patient_id", "medical_record_id", "claim_amount", "claim_status", "submitted_date")
    list_filter = ("claim_status", "submitted_date")
    search_fields = ("patient__username", "medical_record__record_id")
    ordering = ("-submitted_date",)
