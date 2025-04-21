from rest_framework import serializers
from .models import *


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'message']
        read_only_fields = ["user", "created_at"]
