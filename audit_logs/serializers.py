from rest_framework import serializers
from .models import *


class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'timestamp', 'ip_address']
        read_only_fields = ["user", "timestamp", "ip_address"]


class ExternalAPILogSerializer(AuditLogSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ExternalAPILog
        fields = ['id', 'user', 'service_name', 'api_url', 'method', 'response_data', 'timestamp']
        read_only_fields = ['user', 'timestamp', 'response_data', 'service_name', 'api_url', 'method']

