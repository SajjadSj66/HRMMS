from rest_framework import serializers
from .models import *
import logging

logger = logging.getLogger(__name__)


class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = ['user', 'department', 'license_number']
        read_only_fields = ["user", "license_number"]

    def create(self, validated_data):
        nurse = super().create(validated_data)
        user = self.context['request'].user
        logger.info(f"Nurse profile created for user {user.username} with license {nurse.license_number}")
        return nurse

    def update(self, instance, validated_data):
        nurse = super().update(instance, validated_data)
        user = self.context['request'].user
        logger.info(f"Nurse profile updated by user {user.username} (nurse_id={nurse.id})")
        return nurse
