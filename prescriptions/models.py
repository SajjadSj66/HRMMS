from django.db import models
from records.models import MedicalRecord
from users.models import User


# Create your models here.
class Prescription(models.Model):
    record_id = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    prescribed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_prescriptions',
                                      limit_choices_to={'is_staff': True})
    patient_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_prescriptions',
                                limit_choices_to={'is_staff': False})
    medical_details = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    issued_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"Prescription for {self.patient_id} - {self.medical_details}"


class InsuranceClaim(models.Model):
    STATUS_CHOICES = [
        ("Submitted", "Submitted"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    patient_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insurance_claims', limit_choices_to={'is_staff': False})
    medical_record_id = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='insurance_claims')
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    claim_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Submitted')
    submitted_date = models.DateField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Insurance claim {self.id} - {self.claim_status}"
