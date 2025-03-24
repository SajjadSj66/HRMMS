from django.urls import path
from .views import *

urlpatterns = [
    path("", AppointmentAPIView.as_view(), name="appointments"),
    path("appointments/<int:appointment_id>", AppointmentAPIView.as_view(), name="appointment-detail"),
]