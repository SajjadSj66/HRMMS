from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.change_password_url = reverse('change-password')

        self.user_data = {
            "username": "testuser",
            "email": "<EMAIL>",
            "password": "testpassword",
        }

        self.user = User.objects.create_user(
            username=self.user_data["username"],
            email=self.user_data["email"],
            password=self.user_data["password"],
        )

    def test_register_user_success(self):
        data = {
            "username": "newuser",
            "email": "<EMAIL>",
            "password": "newpassword",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)

    def test_register_user_invalid(self):
        data = {
            "username": "",
            "email": "invalid-email",
            "password": "",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_success(self):
        data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_user_invalid(self):
        data = {
            "username": self.user_data["username"],
            "password": "WrongPassword",
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_user_success(self):
        login_response = self.client.post(self.login_url, {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        })
        refresh_token = login_response.data["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")
        response = self.client.post(self.logout_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_success(self):
        self.client.login(username=self.user_data["username"], password=self.user_data["password"])
        self.client.force_authenticate(user=self.user)

        data = {
            "old_password": self.user_data["password"],
            "new_password": "UpdatePassword",
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)