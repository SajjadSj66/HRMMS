from rest_framework import serializers
from .models import *
import logging

logger = logging.getLogger(__name__)


class DoctorSerializer(serializers.ModelSerializer):
    license_number = serializers.CharField(max_length=50)

    def validate_license_number(self, value):
        if Doctor.objects.filter(license_number=value).exists():
            raise serializers.ValidationError({"Detail": "This license number is already in use."})
        return value

    def validate_specialty(self, value):
        if not value.strip():
            raise serializers.ValidationError({"Detail": "Specialty cannot be empty."})
        return value

    def create(self, validated_data):
        doctor = super().create(validated_data)
        user = self.context['request'].user
        logger.info(f"Doctor profile created for user {user.username} with license {doctor.license_number}")
        return doctor

    def update(self, instance, validated_data):
        doctor = super().update(instance, validated_data)
        user = self.context['request'].user
        logger.info(f"Doctor profile updated by user {user.username} (doctor_id={doctor.id})")
        return doctor

    class Meta:
        model = Doctor
        fields = ['user', 'specialty', 'license_number', 'hospital_affiliation']
        read_only_fields = ['user', 'license_number']
