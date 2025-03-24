from rest_framework import serializers
from .models import *

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user_id', 'notification_type', 'message']
        read_only_fields = ["user_id","created_at"]