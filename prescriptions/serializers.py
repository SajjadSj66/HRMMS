from rest_framework import serializers
from .models import *


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"
        read_only_fields = ["prescribed_by", "issued_date"]

    def create(self, validated_data):
        user = self.context["request"].user
        if user.role != "doctor":
            raise serializers.ValidationError("Only doctors can create prescriptions.")
        medical_record = validated_data["medical_record"]
        patient = validated_data["patient_record"]

        if medical_record.patient != patient:
            raise serializers.ValidationError("the prescription's patient must match the medical record's patient")

        validated_data["prescribed_by"] = user
        return super().create(validated_data)


class InsuranceClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        fields = "__all__"
        read_only_fields = ["submitted_date"]
