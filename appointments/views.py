from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *


# Create your views here.
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["appointment_datetime", "status", "doctor"]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Appointment.objects.none()

        if user.role == 'patient':
            return Appointment.objects.filter(patient__user=user)
        elif user.role == 'doctor':
            return Appointment.objects.filter(doctor__user=user)
        elif user.role == 'nurse':
            return Appointment.objects.filter(nurse__user=user)
        return Appointment.objects.all()
