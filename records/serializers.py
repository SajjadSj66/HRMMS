from rest_framework import serializers
from .models import *
from cryptography.fernet import Fernet
from django.conf import settings

cipher = Fernet(settings.ENCRYPTION_KEY.encode())


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['patient_id', 'doctor_id', 'record_date', 'diagnosis', 'treatment', 'notes', 'attachments']
        read_only_fields = ["doctor_id"]

    def create(self, validated_data):
        user = self.context["request"].user
        if not hasattr(user, "doctor"):
            raise serializers.ValidationError("Only doctor can create medical record")

        validated_data["doctor"] = user.doctor
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if instance.doctor != user.doctor:
            raise serializers.ValidationError("Only doctors can update medical records.")
        return super().update(instance, validated_data)


class LabResultSerializer(serializers.ModelSerializer):
    test_result = serializers.CharField(write_only=True)
    decrypted_test_result = serializers.SerializerMethodField()

    class Meta:
        model = LabResult
        fields = ['patient_id', 'doctor_id', 'test_name', 'test_result', 'normal_range', 'test_date', 'comments',
                  'external_ref']
        read_only_fields = ["doctor_id", "test_date"]

    def create(self, validated_data):
        validated_data["test_result"] = cipher.encrypt(validated_data["test_result"].encode())
        return super().create(validated_data)

    def get_decrypted_test_result(self, obj):
        user = self.context["request"].user
        if user == obj.patient or user == obj.doctor:
            return cipher.decrypt(obj.test_result).decode()
        return "Access denied"
