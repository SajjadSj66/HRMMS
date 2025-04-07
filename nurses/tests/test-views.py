from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from nurses.models import Nurse
from rest_framework import status

User = get_user_model()

class NurseAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='nurseuser', password='testpass')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')
        self.client = APIClient()
        self.nurse = Nurse.objects.create(
            user=self.user,
            department='Emergency',
            license_number='LIC12345'
        )
        self.nurse_list_url = "/api/nurses/"

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_get_nurse_list_authenticated_as_user(self):
        self.authenticate(self.user)
        response = self.client.get(self.nurse_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one nurse related to the user

    def test_get_nurse_list_authenticated_as_admin(self):
        self.authenticate(self.admin)
        response = self.client.get(self.nurse_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Admin can see all nurses

    def test_post_nurse_authenticated(self):
        self.authenticate(self.user)
        data = {
            "department": "ICU",
            "license_number": "LIC98765"
        }
        response = self.client.post(self.nurse_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["department"], "ICU")
        self.assertEqual(response.data["license_number"], "LIC98765")
        self.assertEqual(response.data["user"], self.user.id)  # User should be automatically assigned

    def test_post_nurse_unauthenticated(self):
        response = self.client.post(self.nurse_list_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
