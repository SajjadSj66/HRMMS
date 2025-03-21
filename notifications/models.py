from django.db import models
from users.models import User

# Create your models here.
class Notification(models.Model):
    TYPE_CHOICES = [
        ("Appointment", "Appointment"),
        ("LabResult", "LabResult"),
        ("General", "General"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.notification_type}"