from django.utils import timezone
from rest_framework import serializers
from .models import Appointment, User
import logging

logger = logging.getLogger(__name__)

class AppointmentSerializer(serializers.ModelSerializer):
    """Check appointment details"""
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
        read_only_fields = ['status', 'patient']

    def validate_appointment_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError({"Detail": "The appointment is in the past"})
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        appointment = super().create(validated_data)
        logger.info(
            f"Appointment created by user {request.user.username} for patient {appointment.patient.id} at {appointment.appointment_datetime}"
        )
        return appointment
