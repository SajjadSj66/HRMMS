from django.urls import path
from .views import *

urlpatterns = [
    path("", PrescriptionAPIView.as_view(), name="prescriptions"),
    path("insurance-claims/", InsuranceClaimAPIView.as_view(), name="insurance_claims"),
]
