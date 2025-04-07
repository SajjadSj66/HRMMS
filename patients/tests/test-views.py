from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from patients.models import Patient
from datetime import date
from rest_framework import status

User = get_user_model()

class PatientAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')
        self.client = APIClient()
        self.patient = Patient.objects.create(
            user=self.user,
            date_of_birth=date(1990, 1, 1),
            gender="Male",
            contract_number="+1234567890",
            address="123 Street",
            emergency_contract="+0987654321",
            blood_type="A+",
            allergies="None",
            chronic_conditions="None"
        )
        self.patient_detail_url = f"/api/patients/{self.patient.id}/"
        self.patient_list_url = "/api/patients/"

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_get_patient_list_authenticated(self):
        self.authenticate(self.user)
        response = self.client.get(self.patient_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_patient_detail_authenticated(self):
        self.authenticate(self.user)
        response = self.client.get(self.patient_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["address"], self.patient.address)

    def test_create_patient(self):
        self.authenticate(self.user)
        data = {
            "date_of_birth": "1995-06-15",
            "gender": "Female",
            "contract_number": "+111222333",
            "address": "Test Ave",
            "emergency_contract": "+444555666",
            "blood_type": "O+",
            "allergies": "Peanuts",
            "chronic_conditions": "Asthma"
        }
        response = self.client.post(self.patient_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["blood_type"], "O+")

    def test_update_patient_put(self):
        self.authenticate(self.user)
        data = {
            "date_of_birth": "1985-01-01",
            "gender": "Male",
            "contract_number": "+222333444",
            "address": "New Address",
            "emergency_contract": "+555666777",
            "blood_type": "B+",
            "allergies": "Dust",
            "chronic_conditions": "Hypertension"
        }
        response = self.client.put(self.patient_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["address"], "New Address")

    def test_partial_update_patient_patch(self):
        self.authenticate(self.user)
        data = {
            "address": "Partial Update Street"
        }
        response = self.client.patch(self.patient_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["address"], "Partial Update Street")

    def test_delete_patient_as_admin(self):
        self.authenticate(self.admin)
        response = self.client.delete(self.patient_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_patient_as_non_admin(self):
        self.authenticate(self.user)
        response = self.client.delete(self.patient_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
