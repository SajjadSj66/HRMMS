from django.test import TestCase
from django.contrib.auth import get_user_model
from notifications.models import Notification

User = get_user_model()


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_notification(self):
        notification = Notification.objects.create(
            user_id=self.user,
            notification_type="Appointment",
            message="Your appointment is scheduled.",
        )
        self.assertEqual(notification.user_id.username, "testuser")
        self.assertEqual(notification.notification_type, "Appointment")
        self.assertEqual(notification.message, "Your appointment is scheduled.")
        self.assertFalse(notification.is_read)  # Default value should be False

    def test_str_representation(self):
        notification = Notification.objects.create(
            user_id=self.user,
            notification_type="LabResult",
            message="Your lab results are ready.",
        )
        self.assertEqual(str(notification), f"Notification for {self.user.username} - LabResult")

    def test_notification_type_choices(self):
        notification = Notification.objects.create(
            user_id=self.user,
            notification_type="General",
            message="This is a general notification.",
        )
        self.assertEqual(notification.notification_type, "General")

        # Check if invalid type raises error
        with self.assertRaises(ValueError):
            Notification.objects.create(
                user_id=self.user,
                notification_type="InvalidType",  # Invalid notification type
                message="This should raise an error.",
            )
