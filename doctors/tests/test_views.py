from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from doctors.models import Doctor

class DoctorAPIViewTest(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        # Create a doctor associated with this user
        self.doctor_data = {
            "specialty": "Cardiology",
            "license_number": "A12345",
            "hospital_affiliation": "City Hospital"
        }
        self.doctor = Doctor.objects.create(user=self.user, **self.doctor_data)

    def test_get_doctor_profile_authenticated(self):
        """Test if an authenticated user can retrieve their doctor profile."""
        # Log in the user
        self.client.login(username="testuser", password="testpass")
        response = self.client.get('/api/doctors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['specialty'], "Cardiology")
        self.assertEqual(response.data[0]['license_number'], "A12345")
        self.assertEqual(response.data[0]['hospital_affiliation'], "City Hospital")

    def test_get_doctor_profile_no_profile(self):
        """Test if a user without a doctor profile gets an empty response."""
        user_without_doctor = User.objects.create_user(username="user2", password="testpass2")
        self.client.login(username="user2", password="testpass2")
        response = self.client.get('/api/doctors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_post_doctor_create(self):
        """Test if an authenticated user can create a new doctor profile."""
        # Log in the user
        self.client.login(username="testuser", password="testpass")
        new_doctor_data = {
            "specialty": "Neurology",
            "license_number": "B67890",
            "hospital_affiliation": "General Hospital"
        }
        response = self.client.post('/api/doctors/', new_doctor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['specialty'], "Neurology")
        self.assertEqual(response.data['license_number'], "B67890")
        self.assertEqual(response.data['hospital_affiliation'], "General Hospital")

    def test_post_doctor_create_invalid_data(self):
        """Test if creating a doctor profile with invalid data returns a 400 error."""
        # Log in the user
        self.client.login(username="testuser", password="testpass")
        invalid_data = {
            "specialty": "",  # Invalid: empty specialty
            "license_number": "B67890",
            "hospital_affiliation": "General Hospital"
        }
        response = self.client.post('/api/doctors/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("specialty", response.data)
