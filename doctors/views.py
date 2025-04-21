from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .permissions import IsDoctorOrCreateOnly


class DoctorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrCreateOnly]

    def get(self, request):
        doctor = Doctor.objects.filter(user=request.user)
        serializer = DoctorSerializer(doctor, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
