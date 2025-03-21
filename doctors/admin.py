from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("user", "specialty", "license_number", "hospital_affiliation")
    list_filter = ("specialty",)
    search_fields = ("user__username", "specialty", "license_number")
