from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Appointment
from .serializers import AppointmentSerializer
from .permissions import AppointmentPermission

class AppointmentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, AppointmentPermission]

    def get(self, request):
        """List appointments based on user role"""
        user = request.user

        if user.role == 'patient':
            appointments = Appointment.objects.filter(patient=user.patient)
        elif user.role == 'doctor':
            appointments = Appointment.objects.filter(doctor=user.doctor)
        elif user.role == 'nurse':
            appointments = Appointment.objects.filter(nurse=user.nurse)
        else:
            appointments = Appointment.objects.all()

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create appointment (patients only)"""
        serializer = AppointmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(patient=request.user.patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, appointment_id):
        """Update appointment (doctors and nurses only)"""
        appointment = get_object_or_404(Appointment, id=appointment_id)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, appointment_id):
        """Delete appointment (doctors and patients only)"""
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.delete()
        return Response({"Detail": "Appointment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
