from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import MedicalRecord, LabResult
from .serializers import MedicalRecordSerializer, LabResultSerializer
from .tasks import notify_patient_of_lab_result


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "patient":
            return MedicalRecord.objects.filter(patient=user).select_related("doctor")
        elif user.role == "doctor":
            return MedicalRecord.objects.filter(doctor=user).select_related("patient")
        return MedicalRecord.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != "doctor":
            raise PermissionDenied("Only doctors can create medical records.")
        serializer.save(doctor=self.request.user)


class LabResultViewSet(viewsets.ModelViewSet):
    queryset = LabResult.objects.all()
    serializer_class = LabResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "patient":
            return LabResult.objects.filter(patient=user).select_related("doctor")
        elif user.role == "doctor":
            return LabResult.objects.filter(doctor=user).select_related("patient")
        return LabResult.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != "doctor":
            raise PermissionDenied("Only doctors can create lab results.")
        lab_result = serializer.save(doctor=self.request.user)

        notify_patient_of_lab_result.delay(lab_result.id)
