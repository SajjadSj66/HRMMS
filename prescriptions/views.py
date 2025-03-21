from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import *
from .serializers import *

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "patient":
            return Prescription.objects.filter(patient=user).select_related("medical_record", "prescribed_by")
        elif user.role == "doctor":
            return Prescription.objects.filter(prescribed_by=user).select_related("medical_record", "patient")
        return Prescription.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != "doctor":
            raise PermissionDenied("Only doctors can create prescriptions.")
        prescription = serializer.save(prescribed_by=self.request.user)

        if prescription.medical_record.patient != prescription.patient:
            raise serializers.ValidationError("The prescription's patient must match the medical record's patient.")


class InsuranceClaimViewSet(viewsets.ModelViewSet):
    queryset = InsuranceClaim.objects.all()
    serializer_class = InsuranceClaimSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = InsuranceClaim.objects.all()

        if user.role == "patient":
            queryset = queryset.filter(patient=user)
        claim_status = self.request.query_params.get("claim_status")
        if claim_status:
            queryset = queryset.filter(claim_status=claim_status)
        return queryset()

    def perform_create(self, serializer):
        if self.request.user.role != "patient":
            raise PermissionDenied("Only patients can create insurance claims.")
        serializer.save(patient=self.request.user)