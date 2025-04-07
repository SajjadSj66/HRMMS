from rest_framework.test import APITestCase
from doctors.serializers import *
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()


class DoctorSerializerTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.valid_data = {
            "user": self.user.id,
            "specialty": "Cardiology",
            "license_number": "A12345",
            "hospital_affiliation": "City Hospital"
        }
        self.invalid_license_number = "A12345"
        self.invalid_specialty_empty = ""
        self.invalid_specialty_spaces = "   "

    def test_doctor_serializer_valid(self):
        serializer = DoctorSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        doctor = serializer.save()
        self.assertEqual(doctor.user.username, self.user.username)
        self.assertEqual(doctor.specialty, "Cardiology")
        self.assertEqual(doctor.license_number, "A12345")
        self.assertEqual(doctor.hospital_affiliation, "City Hospital")

    def test_doctor_serializer_duplicate_license_number(self):
        # Create the first doctor
        doctor = Doctor.objects.create(**self.valid_data)
        # Try to create another doctor with the same license number
        invalid_data = self.valid_data.copy()
        invalid_data["license_number"] = self.invalid_license_number
        serializer = DoctorSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_doctor_serializer_invalid_specialty_empty(self):
        invalid_data = self.valid_data.copy()
        invalid_data["specialty"] = self.invalid_specialty_empty
        serializer = DoctorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("specialty", serializer.errors)

    def test_doctor_serializer_invalid_specialty_spaces(self):
        invalid_data = self.valid_data.copy()
        invalid_data["specialty"] = self.invalid_specialty_spaces
        serializer = DoctorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("specialty", serializer.errors)
