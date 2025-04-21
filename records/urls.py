from django.urls import path
from .views import *

urlpatterns = [
    path("medical-records/", MedicalRecordAPIView.as_view(), name="medical_records"),
    path("medical-records/<int:record_id>", MedicalRecordAPIView.as_view(), name="medical_records_detail"),
    path("lab-results/", LabResultAPIView.as_view(), name="lab_results"),
    path("lab-results/<int:record_id>", LabResultAPIView.as_view(), name="lab_results_detail"),
]
