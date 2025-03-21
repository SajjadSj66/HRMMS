from django.utils import timezone

from rest_framework import serializers
from .models import *


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate_appointment_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('The appointment is in the past')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            return serializers.ValidationError("Authentication required.")

        if user.is_staff:
            validated_data["doctor"] = user

        else:
            validated_data['patient'] = user

        return super().create(validated_data)
