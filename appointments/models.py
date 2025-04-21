from django.db import models
from users.models import User


# Create your models here.
class StatusChoices(models.TextChoices):
    SCHEDULED = "Scheduled", "Scheduled"
    COMPLETED = "Completed", "Completed"
    CANCELLED = "Cancelled", "Cancelled"


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments',
                                limit_choices_to={'role': 'patient'}, db_index=True, null=True, blank=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments',
                               limit_choices_to={'role': 'doctor'}, db_index=True, null=True, blank=True)
    nurse = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nurse_appointments',
                              limit_choices_to={'role': 'nurse'}, db_index=True, null=True, blank=True)
    appointment_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.SCHEDULED)
    reason = models.TextField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment: {self.patient.username} with {self.doctor.username} on {self.appointment_datetime} ({self.status})"
