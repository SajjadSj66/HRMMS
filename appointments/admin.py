from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "nurse", "appointment_datetime", "status")
    list_filter = ("status", "appointment_datetime")
    search_fields = ("patient__username", "doctor__username", "nurse__username")
