from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.test import TestCase
from django.contrib.auth import get_user_model
from notifications.models import Notification
from notifications.serializers import NotificationSerializer

User = get_user_model()

class NotificationSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.notification_data = {
            "user_id": self.user.id,  # user_id is read-only
            "notification_type": "Appointment",
            "message": "Your appointment is scheduled.",
        }
        self.invalid_notification_data = {
            "user_id": self.user.id,  # user_id is read-only
            "notification_type": "",  # missing notification_type
            "message": "Your appointment is scheduled.",
        }

    def test_valid_notification_serializer(self):
        serializer = NotificationSerializer(data=self.notification_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        validated_data = serializer.validated_data
        self.assertEqual(validated_data["notification_type"], "Appointment")
        self.assertEqual(validated_data["message"], "Your appointment is scheduled.")
        self.assertEqual(validated_data["user_id"], self.user)

    def test_invalid_notification_serializer_missing_notification_type(self):
        serializer = NotificationSerializer(data=self.invalid_notification_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("notification_type", serializer.errors)

    def test_read_only_user_id(self):
        serializer = NotificationSerializer()
        self.assertIn("user_id", serializer.get_fields())
        self.assertTrue(serializer.get_fields()["user_id"].read_only)

    def test_read_only_created_at(self):
        serializer = NotificationSerializer()
        self.assertIn("created_at", serializer.get_fields())
        self.assertTrue(serializer.get_fields()["created_at"].read_only)
