from django.urls import path
from .views import *

urlpatterns = [
    path("audit-trails/", AuditLogAPIView.as_view(), name="audit-logs"),
    path("external-integrations/", ExternalAPILogAPIView.as_view(), name="external-integrations"),
]
