from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import *
from datetime import date


class PatientSerializer(serializers.ModelSerializer):
    """Check Patients Numbers"""
    contract_number = serializers.CharField(
        validators=[RegexValidator(r'^\+?\d{9,15}$', message="Invalid phone number format.")]
    )
    emergency_contract = serializers.CharField(
        validators=[RegexValidator(r'^\+?\d{9,15}$', message="Invalid emergency contact format.")]
    )
    blood_type = serializers.ChoiceField(
        choices=['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'], required=True
    )

    def validate_date_of_birth(self, value):
        """Validate date of birth date"""
        if value >= date.today():
            raise serializers.ValidationError({"date": "Date of birth must be in the past."})
        return value

    class Meta:
        model = Patient
        fields = ["id", "user", "date_of_birth", "gender", "contract_number", "address", "emergency_contract",
                  "blood_type",
                  "allergies", "chronic_conditions"]
        read_only_fields = ["id", "user","blood_type", "allergies"]
        extra_kwargs = {
            'user': {'read_only': True}
        }
