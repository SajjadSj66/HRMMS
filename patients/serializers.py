from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import *
from datetime import date


class PatientSerializer(serializers.ModelSerializer):
    contract_number = serializers.CharField(
        validators=[RegexValidator(r'^\+?\d{9,15}$', message="Invalid phone number format.")]
    )
    emergency_contract = serializers.CharField(
        validators=[RegexValidator(r'^\+?\d{9,15}$', message="Invalid emergency contact format.")]
    )

    def validate_date_of_birth(self, value):
        if value >= date.today():
            raise serializers.ValidationError("Date of birth must be in the past.")
        return value

    def validate_blood_type(self, value):
        valid_blood_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
        if value and value not in valid_blood_types:
            raise serializers.ValidationError("Invalid blood type.")
        return value

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ["user"]
