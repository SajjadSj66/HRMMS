from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"medical-records", MedicalRecordViewSet, basename="medical-records")
router.register(r"lab-results", LabResultViewSet, basename="lab-results")

urlpatterns = [
    path("", include(router.urls)),
]
