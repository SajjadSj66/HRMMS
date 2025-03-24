from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from patients.models import Patient
from .models import *
from .serializers import MedicalRecordSerializer, LabResultSerializer
from .tasks import notify_patient_of_lab_result


class MedicalRecordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == "patient":
            records = MedicalRecord.objects.filter(patient=user.patient_id).select_related("doctor")
        elif user.role == "doctor":
            records = MedicalRecord.objects.filter(doctor=user.doctor_id).select_related("patient")
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.role != "doctor":
            raise PermissionDenied("Only doctors can create medical records")

        patient_id = request.data.get("patient_id")
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response({"error": "Invalid patient ID"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MedicalRecordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(doctor=request.user.doctor, patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, record_id):
        try:
            record = MedicalRecord.objects.get(id=record_id)
        except MedicalRecord.DoesNotExist:
            return Response({"error": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role != "doctor" or request.user.doctor != record.doctor:
            raise PermissionDenied("Only doctors can update medical records")

        serializer = MedicalRecordSerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, record_id):
        try:
            record = MedicalRecord.objects.get(id=record_id)
        except MedicalRecord.DoesNotExist:
            return Response({"error": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role != "admin" and (request.user.role != "doctor" or request.user.doctor != record.doctor):
            raise PermissionDenied("Only doctor who created this or admin can delete it")

        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LabResultAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = self.request.user
        if hasattr(user, "role"):
            if user.role == "patient":
                results = LabResult.objects.filter(patient=user).select_related("doctor")
            elif user.role == "doctor":
                results = LabResult.objects.filter(doctor=user).select_related("patient")
            else:
                return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

            serializer = LabResultSerializer(results, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "User role undefined"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        if request.user.role != "doctor":
            raise PermissionDenied("Only doctors can create lab results.")

        patient_id = request.data.get("patient_id")
        if not patient_id:
            return Response({"error": "Invalid patient ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = User.objects.get(id=patient_id)
        except User.DoesNotExist:
            return Response({"error": "Invalid patient ID"}, status=status.HTTP_400_BAD_REQUEST)

        request_data = request.data.copy()
        request_data["patient"] = patient.id

        serializer = LabResultSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            lab_result = serializer.save(doctor=request.user, patient=patient)
            notify_patient_of_lab_result.delay(lab_result.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            lab_result = LabResult.objects.get(pk=pk)
        except LabResult.DoesNotExist:
            return Response({"error": "Invalid lab result"}, status=status.HTTP_404_NOT_FOUND)

        if request.user != lab_result.doctor and request.user != lab_result.patient:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = LabResultSerializer(lab_result, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            lab_result = LabResult.objects.get(pk=pk)
        except LabResult.DoesNotExist:
            return Response({"error": "Lab result not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user != lab_result.doctor:
            return Response({"error": "Only doctors can delete lab results."}, status=status.HTTP_403_FORBIDDEN)

        lab_result.delete()
        return Response({"message": "Lab result deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
