from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


class PrescriptionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == "patient":
            prescriptions = Prescription.objects.filter(patient=user).select_related("medical_record", "prescribed_by")
        elif user.role == "doctor":
            prescriptions = Prescription.objects.filter(prescribed_by=user).select_related("medical_record", "patient")
        else:
            return Response({"errors": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.role != "doctor":
            raise PermissionDenied("Only doctors can create prescriptions.")

        record_id = request.data.get("record_id")
        if not record_id:
            return Response({"errors": "Missing record id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            medical_record = MedicalRecord.objects.get(id=record_id)
        except MedicalRecord.DoesNotExist:
            return Response({"errors": "Invalid record id"}, status=status.HTTP_400_BAD_REQUEST)

        patient_id = request.data.get("patient_id")
        if not patient_id:
            return Response({"errors": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = User.objects.get(id=patient_id)
        except User.DoesNotExist:
            return Response({"errors": "Invalid patient id"}, status=status.HTTP_400_BAD_REQUEST)

        if medical_record.patient != patient:
            return Response(
                {"patient_id": "The prescription's patient must match the medical record's patient."},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data["prescribed_by"] = request.user.id
        data["issued_date"] = now()
        data["medical_record"] = medical_record.id
        data["patient"] = patient.id

        serializer = PrescriptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsuranceClaimAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        claims = InsuranceClaim.objects.all()

        if user.role == "patient":
            claims = claims.filter(patient=user)
        claim_status = request.query_params.get("claim_status")
        if claim_status:
            claims = claims.filter(claim_status=claim_status)

        serializer = InsuranceClaimSerializer(claims, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.role != "patient":
            raise PermissionDenied("Only patients can create insurance claims.")

        medical_record_id = request.data.get("medical_record_id")
        if not medical_record_id:
            return Response({"medical_record_id": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            medical_record = MedicalRecord.objects.get(id=medical_record_id)
        except MedicalRecord.DoesNotExist:
            return Response({"medical_record_id": "Invalid medical record ID."}, status=status.HTTP_400_BAD_REQUEST)

        if medical_record.patient != request.user:
            return Response({"error": "The insurance claim must be linked to the correct patient's medical record."},
                            status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data["patient"] = request.user.id
        data["submitted_by"] = now()


        serializer = InsuranceClaimSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
