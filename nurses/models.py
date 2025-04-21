from django.db import models
from users.models import User


# Create your models here.
class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nurse', db_index=True)
    department = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Nurse {self.user.username}"
