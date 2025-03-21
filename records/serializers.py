from rest_framework import serializers
from .models import *
from cryptography.fernet import Fernet
from django.conf import settings

cipher = Fernet(settings.ENCRYPTION_KEY.encode())


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = "__all__"
        read_only_fields = ["doctor", "record_date"]

    def create(self, validated_data):
        user = self.context["request"].user
        if user.role != "doctor":
            raise serializers.ValidationError("Only doctors can create medical records.")
        validated_data["doctor"] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if instance.doctor != user:
            raise serializers.ValidationError("Only doctors can update medical records.")
        return super().update(instance, validated_data)


class LabResultSerializer(serializers.ModelSerializer):
    test_result = serializers.SerializerMethodField()

    def create(self, validated_data):
        validated_data["test_result"] = cipher.encrypt(validated_data["test_result"].encode())
        validated_data.pop("test_result")
        return super().create(validated_data)

    def get_test_result(self, obj):
        user = self.context["request"].user
        if user == obj.patient or user == obj.doctor:
            return cipher.decrypt(obj.test_result).decode()
        return "Access denied"

    class Meta:
        model = LabResult
        fields = "__all__"
        read_only_fields = ["doctor", "test_date", "test_result"]
