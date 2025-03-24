from rest_framework import serializers
from .models import *
from django.utils.timezone import now


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"
        read_only_fields = ["prescribed_by", "issued_date"]

    def create(self, validated_data):
        user = self.context["request"].user

        if user.role != "doctor":
            raise serializers.ValidationError("Only doctors can create prescriptions.")

        record_id = self.context["request"].data.get("record_id")
        if not record_id:
            raise serializers.ValidationError({"record_id": "Missing record id."})

        try:
            medical_record = MedicalRecord.objects.get(id=record_id)
        except MedicalRecord.DoesNotExist:
            raise serializers.ValidationError({"record_id": "Invalid record id."})

        patient_id = self.context["request"].data.get("patient_id")
        if not patient_id:
            raise serializers.ValidationError({"patient_id": "Missing patient id."})

        try:
            patient = User.objects.get(id=patient_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"patient_id": "Invalid patient id."})

        if medical_record.patient != patient:
            raise serializers.ValidationError(
                {"patient_id": "The prescription's patient must match the prescription's medical record."}
            )

        validated_data['prescribed_by'] = user
        validated_data['issued_date'] = now()
        validated_data['patient'] = patient
        validated_data['medical_record'] = medical_record

        return super().create(validated_data)

class InsuranceClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        fields = "__all__"
        read_only_fields = ["submitted_date"]

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        if user.role != "patient":
            raise serializers.ValidationError("Only patients can claim insurance.")

        medical_record = validated_data.get("medical_record")
        patient = validated_data.get("patient")

        if medical_record.patient != patient:
            raise serializers.ValidationError("The insurance claim must be linked to the correct patient's medical record.")

        validated_data["submitted_date"] = now()
        return super().create(validated_data)
