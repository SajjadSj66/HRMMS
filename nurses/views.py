from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .permissions import IsStaffOrOwnNurseProfile


# Create your views here.
class NurseAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStaffOrOwnNurseProfile]

    def get(self, request):
        nurses = Nurse.objects.all() if request.user.is_staff else Nurse.objects.filter(user=request.user)
        serializer = NurseSerializer(nurses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NurseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
