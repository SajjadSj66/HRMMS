from django.contrib import admin
from .models import AuditLog

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address')
    list_filter = ('user', 'action', 'timestamp')
    search_fields = ('action', 'user__username', 'ip_address')
    ordering = ('-timestamp',)
    readonly_fields = ('user', 'action', 'timestamp', 'ip_address')

    def has_add_permission(self, request):
        # Disable adding new audit logs from the admin interface
        return False

    def has_delete_permission(self, request, obj=None):
        # Disable deleting audit logs from the admin interface
        return False

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'message', 'is_read', 'created_at')
    list_filter = ('user', 'notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'message', 'notification_type')
    ordering = ('-created_at',)
    readonly_fields = ('user', 'created_at')

    def has_add_permission(self, request):
        # You can disable adding notifications from the admin if necessary
        return True

    def has_delete_permission(self, request, obj=None):
        # Disable deleting notifications if necessary
        return False

admin.site.register(AuditLog, AuditLogAdmin)
