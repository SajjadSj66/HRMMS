from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from audit_logs.models import AuditLog

User = get_user_model()


class AuditLogTests(APITestCase):
    def setUp(self):
        """Create a test admin user and a normal user."""
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass")
        self.normal_user = User.objects.create_user(username="user", password="userpass")

        # Create an audit log entry
        self.audit_log = AuditLog.objects.create(user=self.admin_user, action="Test Action", ip_address="127.0.0.1")

    def test_admin_can_view_audit_logs(self):
        """Admins should be able to retrieve audit logs."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.get("/api/audit-trails/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Ensure at least one log exists

    def test_non_admin_cannot_view_audit_logs(self):
        """Non-admin users should not be able to access audit logs."""
        self.client.login(username="user", password="userpass")
        response = self.client.get("/api/audit-trails/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Permission denied

    def test_non_admin_cannot_modify_audit_logs(self):
        """Non-admin users should not be able to modify audit logs."""
        self.client.login(username="user", password="userpass")
        response = self.client.put(f"/api/audit-trails/{self.audit_log.id}/", {"action": "Hacked!"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Permission denied
