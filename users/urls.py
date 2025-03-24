from django.urls import path
from .views import *


urlpatterns = [
    path('users/', UserAPIView.as_view(), name='users'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
]
