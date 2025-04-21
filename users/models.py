from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserStatus(models.TextChoices):
    PATIENT = "patient", "Patient"
    DOCTOR = "doctor", "Doctor"
    NURSE = "nurse", "Nurse"
    ADMIN = "admin", "Admin"


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=UserStatus.choices, default=UserStatus.PATIENT)

    def __str__(self):
        return f"{self.username} - {self.email} - {self.role}"
