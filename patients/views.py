from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *


# Create your views here.

class PatientAPIView(APIView):
    """دریافت لیست بیماران یا جزئیات یک بیمار خاص"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        if id:
            patient = get_object_or_404(Patient, id=id, user=request.user)
            serializer = PatientSerializer(patient)
        else:
            patients = Patient.objects.filter(user=request.user)
            serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ایجاد یک پروفایل بیمار جدید"""
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """به‌روزرسانی اطلاعات بیمار (تمام فیلدها)"""
        patient = get_object_or_404(Patient, id=id, user=request.user)
        serializer = PatientSerializer(patient, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        """به‌روزرسانی جزئی اطلاعات بیمار (فقط فیلدهای ارسال‌شده)"""
        patient = get_object_or_404(Patient, id=id, user=request.user)
        serializer = PatientSerializer(patient, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """حذف پروفایل بیمار (فقط برای ادمین‌ها)"""
        if not request.user.is_staff:
            return Response({"You do not have permission to delete this patient."},status=status.HTTP_403_FORBIDDEN)

        patient = get_object_or_404(Patient, id=id)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
