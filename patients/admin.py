from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("user", "date_of_birth", "gender", "contract_number", "blood_type")
    list_filter = ("gender", "blood_type", "chronic_conditions")
    search_fields = ("user__username", "contract_number", "blood_type")
