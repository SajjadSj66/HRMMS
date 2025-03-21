from django.db import models
from users.models import User


# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    specialty = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50, unique=True)
    hospital_affiliation = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"DR. {self.user.username} - {self.specialty}"
