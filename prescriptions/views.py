from django.db import transaction
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .permissions import *


class PrescriptionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get(self, request):
        user = request.user
        if user.role == "patient":
            prescriptions = Prescription.objects.filter(patient=user).select_related("record", "prescriber")
        elif user.role == "doctor":
            prescriptions = Prescription.objects.filter(prescriber=user).select_related("record", "patient")
        else:
            return Response({"Detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        serializer = PrescriptionSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InsuranceClaimAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get(self, request):
        user = request.user

        if user.role not in ["patient", "doctor"]:
            return Response({"Detail": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        claims = InsuranceClaim.objects.all()

        if user.role == "patient":
            claims = claims.filter(patient=user)
        claim_status = request.query_params.get("claim_status")
        if claim_status:
            if claim_status not in ClaimStatus.values:
                return Response({"Detail": "Invalid claim status"}, status=status.HTTP_400_BAD_REQUEST)
            claims = claims.filter(claim_status=claim_status)

        serializer = InsuranceClaimSerializer(claims, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        serializer = InsuranceClaimSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
