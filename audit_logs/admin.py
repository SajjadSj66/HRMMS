from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'timestamp', 'ip_address')
    list_filter = ('user', 'timestamp')
    search_fields = ("action", "user__username")

class ExternalAPILogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service_name', 'api_url', 'method', 'timestamp')
    list_filter = ('service_name', 'timestamp')
    search_fields = ("action", "api-url","user__username")