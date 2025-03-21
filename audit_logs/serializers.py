from rest_framework import serializers
from .models import *

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = "__all__"
        read_only_fields = ["user", "timestamp", "ip_address"]
