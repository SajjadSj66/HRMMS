from django.urls import path
from .views import *

urlpatterns = [
    path("", NurseAPIView.as_view(), name="nurses"),
]
