from django.db import models
from users.models import User


# Create your models here.
class GenderStatus(models.TextChoices):
    MALE = "Male", "Male"
    FEMALE = "Female", "Female"
    CHILD = "Child", "Child"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient", db_index=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10 ,choices=GenderStatus.choices, default=GenderStatus.MALE)
    contract_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    emergency_contract = models.CharField(max_length=255)
    blood_type = models.CharField(max_length=5, null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    chronic_conditions = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Patient: {self.user.username}"
