from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *


# Create your views here.
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'doctor'):
            return Doctor.objects.filter(user=self.request.user)
        return Doctor.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
