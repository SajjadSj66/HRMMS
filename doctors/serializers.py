from rest_framework import serializers
from .models import *


class DoctorSerializer(serializers.ModelSerializer):
    license_number = serializers.CharField(max_length=50)

    def validate_license_number(self, value):
        if Doctor.objects.filter(license_number=value).exists():
            raise serializers.ValidationError("This license number is already in use.")
        return value

    def validated_specialty(self, value):
        if not value.strip():
            raise serializers.ValidationError("Specialty cannot be empty.")
        return value

    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ["user"]
