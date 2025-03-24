from django.urls import path
from .views import *

urlpatterns = [
    path("", DoctorAPIView.as_view(), name="doctors"),
]
