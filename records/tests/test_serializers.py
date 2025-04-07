import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from records.models import MedicalRecord, LabResult
from records.serializers import MedicalRecordSerializer, LabResultSerializer
from doctors.models import Doctor
from patients.models import Patient
from cryptography.fernet import Fernet
from django.conf import settings

User = get_user_model()
cipher = Fernet(settings.ENCRYPTION_KEY.encode())


@pytest.mark.django_db
class TestMedicalRecordSerializer:

    def setup_method(self):
        self.factory = APIRequestFactory()
        self.patient_user = User.objects.create_user(username='patient', password='pass', role='patient')
        self.patient = Patient.objects.create(user=self.patient_user)

        self.doctor_user = User.objects.create_user(username='doctor', password='pass', role='doctor')
        self.doctor = Doctor.objects.create(user=self.doctor_user)

    def test_create_medical_record_as_doctor(self):
        request = self.factory.post('/medical-records/')
        request.user = self.doctor_user

        data = {
            "patient_id": self.patient.id,
            "record_date": "2025-04-07",
            "diagnosis": "Flu",
            "treatment": "Rest and hydration",
            "notes": "Follow up in 3 days",
            "attachments": None
        }

        serializer = MedicalRecordSerializer(data=data, context={"request": request})
        assert serializer.is_valid(), serializer.errors
        instance = serializer.save()
        assert instance.doctor == self.doctor

    def test_create_medical_record_as_non_doctor(self):
        request = self.factory.post('/medical-records/')
        request.user = self.patient_user

        data = {
            "patient_id": self.patient.id,
            "record_date": "2025-04-07",
            "diagnosis": "Flu",
            "treatment": "Rest and hydration",
            "notes": "Follow up in 3 days",
            "attachments": None
        }

        serializer = MedicalRecordSerializer(data=data, context={"request": request})
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors


@pytest.mark.django_db
class TestLabResultSerializer:

    def setup_method(self):
        self.factory = APIRequestFactory()

        self.patient_user = User.objects.create_user(username='puser', password='pass', role='patient')
        self.patient = Patient.objects.create(user=self.patient_user)

        self.doctor_user = User.objects.create_user(username='duser', password='pass', role='doctor')
        self.doctor = Doctor.objects.create(user=self.doctor_user)

    def test_create_lab_result_encrypts_result(self):
        request = self.factory.post('/lab-results/')
        request.user = self.doctor_user

        data = {
            "patient_id": self.patient.id,
            "test_name": "Blood Test",
            "test_result": "High cholesterol",
            "normal_range": "Normal",
            "comments": "Check again in 1 month",
            "external_ref": "REF123"
        }

        serializer = LabResultSerializer(data=data, context={"request": request})
        assert serializer.is_valid(), serializer.errors
        result = serializer.save(doctor=self.doctor)
        assert result.test_result != "High cholesterol"
        decrypted = cipher.decrypt(result.test_result).decode()
        assert decrypted == "High cholesterol"

    def test_decrypted_result_visible_to_authorized_users(self):
        encrypted_result = cipher.encrypt(b"Low iron")
        result = LabResult.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            test_name="Iron Test",
            test_result=encrypted_result,
            normal_range="Normal",
            comments="Follow up",
            external_ref="IRON123"
        )

        request = self.factory.get('/lab-results/')
        request.user = self.patient_user

        serializer = LabResultSerializer(instance=result, context={"request": request})
        assert serializer.data["decrypted_test_result"] == "Low iron"

    def test_decrypted_result_hidden_from_unauthorized_user(self):
        # another unrelated user
        other_user = User.objects.create_user(username='intruder', password='pass', role='nurse')
        encrypted_result = cipher.encrypt(b"Sensitive info")
        result = LabResult.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            test_name="Confidential Test",
            test_result=encrypted_result,
            normal_range="Normal",
            comments="Sensitive",
            external_ref="SENS123"
        )

        request = self.factory.get('/lab-results/')
        request.user = other_user

        serializer = LabResultSerializer(instance=result, context={"request": request})
        assert serializer.data["decrypted_test_result"] == "Access denied"
