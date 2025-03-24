from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from audit_logs.models import ExternalAPILog
from audit_logs.views import ExternalAPILogAPIView

User = get_user_model()

class ExternalAPILogTests(APITestCase):
    def setUp(self):
        """Create a test admin user."""
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass")

    @patch("requests.get")  # Mock requests.get to avoid real API calls
    def test_external_api_logging(self, mock_get):
        """Test that external API calls are logged correctly."""
        self.client.login(username="admin", password="adminpass")

        # Mock response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"message": "Success"}

        # Simulate an API call (e.g., calling an external pharmacy API)
        response = self.client.get("/api/external-integrations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that an external API log entry was created
        self.assertTrue(ExternalAPILog.objects.exists())

    @patch("requests.get")
    def test_external_api_logging_failure(self, mock_get):
        """Test logging when an external API fails."""
        self.client.login(username="admin", password="adminpass")

        # Mock API failure response
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {"error": "Server error"}

        response = self.client.get("/api/external-integrations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # App should still function

        # Verify that a failure log is recorded
        log = ExternalAPILog.objects.last()
        self.assertIn("error", log.response_data)  # Ensure error response is logged
