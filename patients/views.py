from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from .permissions import IsOwnerOrAdminCanDelete


# Create your views here.

class PatientAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminCanDelete]

    def get_object(self, id):
        return get_object_or_404(Patient, id=id)

    def get(self, request, id=None):
        if id:
            patient = self.get_object(id)
            self.check_object_permissions(request, patient)
            serializer = PatientSerializer(patient)
        else:
            patients = Patient.objects.filter(user=request.user)
            serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        patient = self.get_object(id)
        self.check_object_permissions(request, patient)
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        patient = self.get_object(id)
        self.check_object_permissions(request, patient)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        patient = self.get_object(id)
        self.check_object_permissions(request, patient)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
