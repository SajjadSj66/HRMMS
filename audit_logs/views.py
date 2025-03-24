from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


class AuditLogAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        if request.user.is_superuser:
            logs = AuditLog.objects.all().order_by('-timestamp')
        else:
            logs = AuditLog.objects.filter(user=request.user).order_by('-timestamp')

        serializer = AuditLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExternalAPILogAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        if request.user.is_superuser:
            api = ExternalAPILog.objects.all().order_by('-timestamp')
        else:
            api = ExternalAPILog.objects.filter(user=request.user).order_by('-timestamp')

        serializer = ExternalAPILogSerializer(api, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
