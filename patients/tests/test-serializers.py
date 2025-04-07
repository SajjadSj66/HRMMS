from rest_framework.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from patients.models import Patient
from patients.serializers import PatientSerializer
from datetime import date, timedelta

User = get_user_model()

class PatientSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testpatient",
            email="test@patient.com",
            password="strongpass123"
        )
        self.valid_data = {
            "user": self.user.id,  # user is read-only; we can simulate assignment manually
            "date_of_birth": "1990-05-21",
            "gender": "Male",
            "contract_number": "+12345678901",
            "address": "123 Test St, Testville",
            "emergency_contract": "+10987654321",
            "blood_type": "O+",
            "allergies": "Pollen",
            "chronic_conditions": "Diabetes"
        }

    def test_valid_serializer(self):
        serializer = PatientSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_contract_number(self):
        data = self.valid_data.copy()
        data["contract_number"] = "invalid_number"
        serializer = PatientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("contract_number", serializer.errors)

    def test_invalid_emergency_contact(self):
        data = self.valid_data.copy()
        data["emergency_contract"] = "emergency123"
        serializer = PatientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("emergency_contract", serializer.errors)

    def test_invalid_blood_type(self):
        data = self.valid_data.copy()
        data["blood_type"] = "X+"  # not in choices
        serializer = PatientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("blood_type", serializer.errors)

    def test_invalid_date_of_birth_future(self):
        data = self.valid_data.copy()
        data["date_of_birth"] = (date.today() + timedelta(days=1)).isoformat()
        serializer = PatientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("date_of_birth", serializer.errors)

    def test_user_field_is_read_only(self):
        serializer = PatientSerializer()
        self.assertIn("user", serializer.get_fields())
        self.assertTrue(serializer.get_fields()["user"].read_only)
