from django.urls import path
from .views import *

urlpatterns = [
    path("", PatientAPIView.as_view(), name="patients"),
    path("patients/<int:id>", PatientAPIView.as_view(), name="patients-detail"),


]