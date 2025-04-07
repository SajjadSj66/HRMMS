from django.test import TestCase
from django.contrib.auth import get_user_model
from nurses.models import Nurse
from django.db import IntegrityError

User = get_user_model()

class NurseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='nurse1', password='testpass')
        self.another_user = User.objects.create_user(username='nurse2', password='testpass')

    def test_create_nurse(self):
        nurse = Nurse.objects.create(
            user=self.user,
            department='Emergency',
            license_number='LIC12345'
        )
        self.assertEqual(nurse.department, 'Emergency')
        self.assertEqual(nurse.license_number, 'LIC12345')
        self.assertEqual(nurse.user.username, 'nurse1')

    def test_str_representation(self):
        nurse = Nurse.objects.create(
            user=self.user,
            department='ICU',
            license_number='LIC99999'
        )
        self.assertEqual(str(nurse), f"Nurse {self.user.username}")

    def test_license_number_unique(self):
        Nurse.objects.create(
            user=self.user,
            department='Pediatrics',
            license_number='UNIQUE123'
        )
        with self.assertRaises(IntegrityError):
            Nurse.objects.create(
                user=self.another_user,
                department='Surgery',
                license_number='UNIQUE123'  # Duplicate
            )
