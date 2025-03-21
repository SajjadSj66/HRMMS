from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ('user', 'department',"license_number")
    search_fields = ("user__username", "license_number")