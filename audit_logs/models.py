from django.db import models
from users.models import User


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Audit Log: {self.action} by {self.user}"

    @classmethod
    def log_external_api_call(cls, user, service_name, api_url, method, request_data=None):
        action = f"External API call: {service_name} - {method} {api_url}"
        cls.objects.create(user=user, action=action)
