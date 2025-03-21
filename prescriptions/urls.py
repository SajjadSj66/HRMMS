from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"prescriptions", PrescriptionViewSet, basename="prescriptions")
router.register(r"insurance-claims", InsuranceClaimViewSet, basename="insurance-claims")

urlpatterns = [
    path("", include(router.urls)),
]
