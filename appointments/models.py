from django.db import models
from users.models import User


# Create your models here.
class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments',
                                limit_choices_to={'is_staff': False})
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments',
                               limit_choices_to={'is_staff': True})
    nurse = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='nurse_appointments')
    appointment_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    reason = models.TextField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment: {self.patient.username} with {self.doctor.username} on {self.appointment_datetime} ({self.status})"
