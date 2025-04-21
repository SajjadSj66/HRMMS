import logging
from rest_framework import serializers
from .models import *
from django.utils.timezone import now

logger = logging.getLogger(__name__)


class PrescriptionSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(write_only=True)
    patient_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Prescription
        fields = [
            "id", "record", "prescriber", "patient",
            "medical_details", "dosage", "frequency", "duration",
            "notes", "issued_date",
            "record_id", "patient_id"
        ]
        read_only_fields = ["id", "prescriber", "issued_date", "record", "patient"]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user

        # Getting values from input
        record_id = attrs.get("record_id")
        patient_id = attrs.get("patient_id")

        if not record_id:
            raise serializers.ValidationError({"record_id": "This field is required."})
        if not patient_id:
            raise serializers.ValidationError({"patient_id": "This field is required."})

        try:
            record = MedicalRecord.objects.get(id=record_id)
        except MedicalRecord.DoesNotExist:
            raise serializers.ValidationError({"record_id": "Invalid record id."})

        try:
            patient = User.objects.get(id=patient_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"patient_id": "Invalid patient id."})

        if record.patient != patient:
            raise serializers.ValidationError({
                "patient_id": "The patient must match the medical record's patient."
            })

        # Save in context for use in create
        self.context["record"] = record
        self.context["patient"] = patient

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        record = self.context["record"]
        patient = self.context["patient"]

        validated_data["prescriber"] = user
        validated_data["issued_date"] = now()
        validated_data["record"] = record
        validated_data["patient"] = patient

        prescription = Prescription.objects.create(**validated_data)

        logger.info(f"Prescription created by user {user.id}, prescription id: {prescription.id}")

        return prescription


class InsuranceClaimSerializer(serializers.ModelSerializer):
    medical_record_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = InsuranceClaim
        fields = [
            "id", "patient", "medical_record", "claim_amount", "claim_status",
            "submitted_date", "notes", "medical_record_id"
        ]
        read_only_fields = ["id", "patient", "medical_record", "claim_amount", "submitted_date"]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user

        record_id = attrs.get("medical_record_id")
        if not record_id:
            raise serializers.ValidationError({"medical_record_id": "This field is required."})

        try:
            record = MedicalRecord.objects.get(id=record_id)
        except MedicalRecord.DoesNotExist:
            raise serializers.ValidationError({"medical_record_id": "Invalid ID."})

        if record.patient != user:
            raise serializers.ValidationError({
                "medical_record_id": "The medical record must belong to the requesting patient."
            })

        # Save to create
        self.context["record"] = record

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        record = self.context["record"]

        validated_data["patient"] = request.user
        validated_data["medical_record"] = record
        validated_data["submitted_date"] = now().date()

        claim = InsuranceClaim.objects.create(**validated_data)

        logger.info(f"Insurance claim submitted by user {request.user.id}, claim ID: {claim.id}")
        return claim
