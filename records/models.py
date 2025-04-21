from django.db import models
from rest_framework.exceptions import ValidationError
from users.models import User
from cryptography.fernet import Fernet
from django.conf import settings


# Create your models here.
class MedicalRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_patient',
                                limit_choices_to={'role': 'patient'}, db_index=True, null=True, blank=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_medical_patient',
                               limit_choices_to={'role': 'doctor'}, db_index=True, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True, null=True)
    attachments = models.FileField(upload_to="medical_records/", blank=True, null=True)

    def clean(self):
        if self.patient.is_staff:
            raise ValidationError({'patient': 'You are not allowed to medical records.'})
        if not self.doctor.is_staff:
            raise ValidationError({'doctor': 'Doctors must be staff members.'})

    def __str__(self):
        return f"Record for {self.patient_id} - {self.record_date}"


if not hasattr(settings, "ENCRYPTION_KEY"):
    raise ValueError("ENCRYPTION_KEY must be set in settings.py")

cipher = Fernet(settings.ENCRYPTION_KEY.encode())


class LabResult(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lab_result',
                                limit_choices_to={'role': 'patient'}, db_index=True, null=True, blank=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_lab_result',
                               limit_choices_to={'role': 'doctor'}, db_index=True, null=True, blank=True)
    test_name = models.CharField(max_length=255)
    test_result = models.BinaryField(null=True, blank=True, db_column="_test_result")
    normal_range = models.CharField(max_length=100)
    test_date = models.DateField()
    comments = models.TextField(null=True, blank=True)
    external_ref = models.CharField(max_length=50, unique=True)

    def get_test_result(self):
        return cipher.decrypt(self.test_result).decode()

    def set_test_result(self, value):
        self.test_result = cipher.encrypt(value.encode())

    _test_result = property(get_test_result, set_test_result)
