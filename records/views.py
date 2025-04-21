from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from patients.models import Patient
from .models import *
from .serializers import MedicalRecordSerializer, LabResultSerializer
from .tasks import notify_patient_of_lab_result
from .permissions import *


class MedicalRecordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsDoctor()]
        elif self.request.method in ["PUT", "PATCH"]:
            return [permissions.IsAuthenticated(), IsOwnerDoctorOfRecord()]
        elif self.request.method == "DELETE":
            return [permissions.IsAuthenticated(), IsDoctorOrAdminForDelete()]
        return [permissions.IsAuthenticated()]

    def get(self, request):
        user = request.user
        if user.role == "patient":
            records = MedicalRecord.objects.filter(patient=user.patient_id).select_related("doctor")
        elif user.role == "doctor":
            records = MedicalRecord.objects.filter(doctor=user.doctor_id).select_related("patient")
        else:
            return Response({"Detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        patient_id = request.data.get("patient_id")
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response({"Detail": "Invalid patient ID"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MedicalRecordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, record_id):
        try:
            record = MedicalRecord.objects.get(id=record_id)
        except MedicalRecord.DoesNotExist:
            return Response({"Detail": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, record)

        serializer = MedicalRecordSerializer(record, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, record_id):
        try:
            record = MedicalRecord.objects.get(id=record_id)
        except MedicalRecord.DoesNotExist:
            return Response({"Detail": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, record)

        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LabResultAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if hasattr(user, "role"):
            if user.role == "patient":
                results = LabResult.objects.filter(patient=user).select_related("doctor")
            elif user.role == "doctor":
                results = LabResult.objects.filter(doctor=user).select_related("patient")
            else:
                return Response({"Detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

            serializer = LabResultSerializer(results, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"Detail": "User role undefined"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        self.check_permissions(request)
        if not IsDoctor().has_permission(request, self):
            raise PermissionDenied("Only doctors can create lab results.")

        patient_id = request.data.get("patient_id")
        if not patient_id:
            return Response({"Detail": "Invalid patient ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = User.objects.get(id=patient_id)
        except User.DoesNotExist:
            return Response({"Detail": "Invalid patient ID"}, status=status.HTTP_400_BAD_REQUEST)

        request_data = request.data.copy()
        request_data["patient"] = patient.id

        serializer = LabResultSerializer(data=request_data, context={"request": request})
        if serializer.is_valid():
            lab_result = serializer.save(doctor=request.user, patient=patient)
            notify_patient_of_lab_result.delay(lab_result.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, record_id):
        try:
            lab_result = LabResult.objects.get(pk=record_id)
        except LabResult.DoesNotExist:
            return Response({"Detail": "Invalid lab result"}, status=status.HTTP_404_NOT_FOUND)

        if not IsDoctorOrPatient().has_object_permission(request, self, lab_result):
            return Response({"Detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = LabResultSerializer(lab_result, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, record_id):
        try:
            lab_result = LabResult.objects.get(pk=record_id)
        except LabResult.DoesNotExist:
            return Response({"Detail": "Lab result not found"}, status=status.HTTP_404_NOT_FOUND)

        if not IsDoctorAndOwner().has_object_permission(request, self, lab_result):
            return Response({"Detail": "Only doctors can delete lab results."}, status=status.HTTP_403_FORBIDDEN)

        lab_result.delete()
        return Response({"Detail": "Lab result deleted successfully"}, status=status.HTTP_204_NO_CONTENT)