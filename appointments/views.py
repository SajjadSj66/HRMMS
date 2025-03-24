from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


# Create your views here.
class AppointmentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """نمایش لیست نوبت‌های مربوط به کاربر"""
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
        """ایجاد نوبت جدید (فقط بیماران)"""
        if not hasattr(request.user, 'patient'):
            return Response({"error": "Only patients can create an appointment."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=request.user.patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, appointment_id):
        """بروزرسانی نوبت (فقط پزشک و پرستار)"""
        appointment = get_object_or_404(Appointment, id=appointment_id)

        if not (hasattr(request.user, 'doctor') or hasattr(request.user, 'nurse')):
            return Response({"error": "Only doctors and nurses can update appointments."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete(self, request, appointment_id):
    """حذف نوبت (فقط پزشک و بیمار)"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if not(hasattr(request.user, 'doctor') or hasattr(request.user, 'patient')):
        return Response({"error": "Only doctors and patients can delete appointments."},
                        status=status.HTTP_403_FORBIDDEN)

    appointment.delete()
    return Response({"message": "Appointment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
