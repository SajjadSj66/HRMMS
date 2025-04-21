from django.core.validators import MinValueValidator
from django.db import models
from records.models import MedicalRecord
from users.models import User


# Create your models here.
class Prescription(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions', db_index=True)
    prescriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_prescriptions',
                                   limit_choices_to={'role': 'doctor'}, db_index=True, null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_prescriptions',
                                limit_choices_to={'role': 'patient'}, db_index=True, null=True, blank=True)
    medical_details = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    issued_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient_id} - {self.medical_details}"


class ClaimStatus(models.TextChoices):
    SUBMITTED = "Submitted", "Submitted"
    APPROVED = "Approved", "Approved"
    REJECTED = "Rejected", "Rejected"


class InsuranceClaim(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insurance_claims',
                                limit_choices_to={'role': 'patient'}, db_index=True, null=True, blank=True)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='insurance_claims', db_index=True)
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    claim_status = models.CharField(choices=ClaimStatus.choices, default=ClaimStatus.SUBMITTED, max_length=50)
    submitted_date = models.DateField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Insurance claim {self.id} - {self.claim_status}"
