from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from records.models import MedicalRecord, LabResult
from patients.models import Patient
from datetime import date
import uuid

class MedicalRecordViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Users
        self.doctor_user = User.objects.create_user(username="doc", password="pass", role="doctor", is_staff=True)
        self.patient_user = User.objects.create_user(username="pat", password="pass", role="patient", is_staff=False)
        self.admin_user = User.objects.create_superuser(username="admin", password="pass", role="admin")

        # Assign related models
        self.patient = Patient.objects.create(user=self.patient_user, phone="123", address="Test")

        self.medical_record = MedicalRecord.objects.create(
            patient_id=self.patient_user,
            doctor_id=self.doctor_user,
            diagnosis="Test",
            treatment="Treatment"
        )

    def test_patient_can_get_own_medical_records(self):
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get("/api/records/medical/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_doctor_can_create_medical_record(self):
        self.client.force_authenticate(user=self.doctor_user)
        data = {
            "patient_id": self.patient.id,
            "diagnosis": "New Diagnosis",
            "treatment": "New Treatment"
        }
        response = self.client.post("/api/records/medical/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_doctor_cannot_create_medical_record(self):
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.post("/api/records/medical/", data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_doctor_can_update_own_medical_record(self):
        self.client.force_authenticate(user=self.doctor_user)
        data = {"diagnosis": "Updated Diagnosis"}
        response = self.client.put(f"/api/records/medical/{self.medical_record.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_owner_doctor_cannot_update_medical_record(self):
        other_doc = User.objects.create_user(username="otherdoc", password="pass", role="doctor", is_staff=True)
        self.client.force_authenticate(user=other_doc)
        response = self.client.put(f"/api/records/medical/{self.medical_record.id}/", data={"diagnosis": "X"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LabResultViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.doctor = User.objects.create_user(username="doctor", password="pass", role="doctor", is_staff=True)
        self.patient = User.objects.create_user(username="patient", password="pass", role="patient", is_staff=False)

        self.lab_result = LabResult.objects.create(
            patient_id=self.patient,
            doctor_id=self.doctor,
            test_name="CBC",
            normal_range="4-10",
            test_date=date.today(),
            external_ref=str(uuid.uuid4())
        )
        self.lab_result._test_result = "Encrypted Test Result"
        self.lab_result.save()

    def test_patient_can_view_own_lab_results(self):
        self.client.force_authenticate(user=self.patient)
        response = self.client.get("/api/records/lab/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_doctor_can_create_lab_result(self):
        self.client.force_authenticate(user=self.doctor)
        data = {
            "patient_id": self.patient.id,
            "test_name": "X-Ray",
            "test_result": "Test Result",
            "normal_range": "1-10",
            "test_date": date.today(),
            "external_ref": str(uuid.uuid4())
        }
        response = self.client.post("/api/records/lab/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patient_cannot_create_lab_result(self):
        self.client.force_authenticate(user=self.patient)
        response = self.client.post("/api/records/lab/", data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_doctor_can_delete_lab_result(self):
        self.client.force_authenticate(user=self.doctor)
        response = self.client.delete(f"/api/records/lab/{self.lab_result.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
