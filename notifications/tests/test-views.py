from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from notifications.models import Notification
from rest_framework import status

User = get_user_model()

class NotificationAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')
        self.client = APIClient()
        self.notification_data = {
            "notification_type": "Appointment",
            "message": "Your appointment is scheduled."
        }
        self.notification = Notification.objects.create(
            user_id=self.user,
            notification_type="LabResult",
            message="Your lab results are ready.",
        )
        self.notification_url = "/api/notifications/"

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_get_notifications_authenticated(self):
        self.authenticate(self.user)
        response = self.client.get(self.notification_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one notification related to the user

    def test_get_notifications_unauthenticated(self):
        response = self.client.get(self.notification_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_notification_authenticated(self):
        self.authenticate(self.user)
        data = {
            "notification_type": "General",
            "message": "This is a general notification."
        }
        response = self.client.post(self.notification_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["notification_type"], "General")
        self.assertEqual(response.data["message"], "This is a general notification.")
        self.assertEqual(response.data["user_id"], self.user.id)  # user_id should match the authenticated user

    def test_post_notification_unauthenticated(self):
        response = self.client.post(self.notification_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_notification_invalid_data(self):
        self.authenticate(self.user)
        data = {
            "notification_type": "",  # Missing notification type
            "message": "This should fail."
        }
        response = self.client.post(self.notification_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("notification_type", response.data)  # Check for the validation error for missing notification type
