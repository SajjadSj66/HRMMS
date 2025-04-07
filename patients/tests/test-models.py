from django.test import TestCase
from django.contrib.auth import get_user_model
from patients.models import Patient
from datetime import date

User = get_user_model()

class PatientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testpatient",
            email="test@patient.com",
            password="strongpass123"
        )
        self.patient = Patient.objects.create(
            user=self.user,
            date_of_birth=date(1990, 5, 21),
            gender="Male",
            contract_number="1234567890",
            address="123 Test St, Testville",
            emergency_contract="Mom: 1234567890",
            blood_type="O+",
            allergies="Peanuts",
            chronic_conditions="Asthma"
        )

    def test_patient_str(self):
        self.assertEqual(str(self.patient), f"Patient: {self.user.username}")

    def test_patient_fields(self):
        self.assertEqual(self.patient.date_of_birth, date(1990, 5, 21))
        self.assertEqual(self.patient.gender, "Male")
        self.assertEqual(self.patient.contract_number, "1234567890")
        self.assertEqual(self.patient.address, "123 Test St, Testville")
        self.assertEqual(self.patient.emergency_contract, "Mom: 1234567890")
        self.assertEqual(self.patient.blood_type, "O+")
        self.assertEqual(self.patient.allergies, "Peanuts")
        self.assertEqual(self.patient.chronic_conditions, "Asthma")
