from django.template.context_processors import request
from django.utils import timezone
from rest_framework import serializers
from .models import *


class AppointmentSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='patient'), source='patient', write_only=True
    )

    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='doctor'), source='doctor', write_only=True
    )

    nurse_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='nurse'), source='nurse', write_only=True
    )

    class Meta:
        model = Appointment
        fields = ['patient_id', 'doctor_id', 'nurse_id', 'appointment_datetime', 'status', 'reason', 'notes']

    def validate_appointment_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('The appointment is in the past')
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError('You are not logged in')

        return super().create(validated_data)
