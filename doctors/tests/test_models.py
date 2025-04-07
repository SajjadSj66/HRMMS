from django.test import TestCase
from django.contrib.auth import get_user_model
from doctors.models import Doctor
from django.db.utils import IntegrityError

User = get_user_model()


class DoctorModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.doctor_data = {
            "user": self.user,
            "specialty": "Cardiology",
            "license_number": "A12345",
            "hospital_affiliation": "City Hospital"
        }
        self.doctor = Doctor.objects.create(**self.doctor_data)

    def test_doctor_creation(self):
        doctor = Doctor.objects.get(user=self.user)
        self.assertEqual(doctor.user.username, self.user.username)
        self.assertEqual(doctor.specialty, "Cardiology")
        self.assertEqual(doctor.license_number, "A12345")
        self.assertEqual(doctor.hospital_affiliation, "City Hospital")

    def test_doctor_str_method(self):
        doctor = Doctor.objects.get(user=self.user)
        self.assertEqual(str(doctor), f"DR. {self.user.username} - Cardiology")

    def test_unique_license_number(self):
        # Attempting to create a doctor with a duplicate license_number
        with self.assertRaises(IntegrityError):
            duplicate_doctor = Doctor.objects.create(
                user=self.user,
                specialty="Neurology",
                license_number="A12345",  # Duplicate license number
                hospital_affiliation="General Hospital"
            )
