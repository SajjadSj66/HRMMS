from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


# Create your views here.
class DoctorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if hasattr(request.user, 'doctor'):
            doctor = Doctor.objects.filter(user=request.user)
        else:
            doctor = Doctor.objects.none()

        serializer = DoctorSerializer(doctor, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
