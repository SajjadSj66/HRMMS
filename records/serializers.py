from rest_framework import serializers
from .models import *
from cryptography.fernet import Fernet
from django.conf import settings
import logging
from .permissions import IsDoctorOrPatient

cipher = Fernet(settings.ENCRYPTION_KEY.encode())

logger = logging.getLogger(__name__)

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'doctor', 'record_date', 'diagnosis', 'treatment', 'notes', 'attachments']
        read_only_fields = ["doctor", "record_date"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["doctor"] = user.doctor
        record = super().create(validated_data)
        logger.info(f"Medical Record created by doctor {user.doctor} for patient {record.patient.id} (record_id-{record.id})")
        return record

    def update(self, instance, validated_data):
        record = super().update(instance, validated_data)
        logger.info(f"MedicalRecord {record.id} updated by doctor {self.context['request'].user.username}")
        return record

class LabResultSerializer(serializers.ModelSerializer):
    test_result = serializers.CharField(write_only=True)
    decrypted_test_result = serializers.SerializerMethodField()

    class Meta:
        model = LabResult
        fields = ['patient', 'doctor', 'test_name', 'test_result', 'normal_range', 'test_date', 'comments',
                  'external_ref']
        read_only_fields = ["doctor", "test_date", "test_result"]

    def create(self, validated_data):
        # Encrypt test results before saving
        validated_data["test_result"] = cipher.encrypt(validated_data["test_result"].encode())
        lab_result = super().create(validated_data)

        user = self.context["request"].user
        logger.info(
            f"LabResult created by doctor {user.username} for patient {lab_result.patient.id} (test={lab_result.test_name})"
        )
        return lab_result

    def get_decrypted_test_result(self, obj):
        """Display the decoded result only to the patient or doctor"""
        request = self.context.get("request")
        if request and IsDoctorOrPatient().has_object_permission(request, None, obj):
            return cipher.decrypt(obj.test_result).decode()
        return "Access denied"


def get_decrypted_test_result(self, obj):
    """Get the decrypted test result."""
    user = self.context["request"].user
    if user == obj.patient or user == obj.doctor:
        return cipher.decrypt(obj.test_result).decode()
    return "Access denied"
