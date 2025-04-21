from django.db import models
from users.models import User


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs", db_index=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Audit Log: {self.action} by {self.user}"


class ExternalAPILog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="external_api_logs", db_index=True)
    service_name = models.CharField(max_length=255)
    api_url = models.URLField()
    method = models.CharField(max_length=10)
    request_data = models.JSONField(null=True, blank=True)
    response_data = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.service_name} - {self.method}] {self.api_url}"

    @classmethod
    def log_external_api_call(cls, user, service_name, api_url, method, request_data=None, response_data=None):
        cls.objects.create(user=user,
                           service_name=service_name,
                           api_url=api_url,
                           method=method,
                           request_data=request_data,
                           response_data=response_data)
