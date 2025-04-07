from django.test import TestCase
from django.contrib.auth import get_user_model
from nurses.serializers import NurseSerializer

User = get_user_model()

class NurseSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="nurseuser", password="nursepass")
        self.nurse_data = {
            "user": self.user.id,  # user field is read-only
            "department": "Emergency",
            "license_number": "LIC98765"
        }
        self.invalid_nurse_data = {
            "user": self.user.id,  # user field is read-only
            "department": "",  # missing department
            "license_number": "LIC12345"
        }

    def test_valid_nurse_serializer(self):
        serializer = NurseSerializer(data=self.nurse_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        validated_data = serializer.validated_data
        self.assertEqual(validated_data["department"], "Emergency")
        self.assertEqual(validated_data["license_number"], "LIC98765")
        self.assertEqual(validated_data["user"], self.user)

    def test_invalid_nurse_serializer_missing_department(self):
        serializer = NurseSerializer(data=self.invalid_nurse_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("department", serializer.errors)

    def test_user_field_is_read_only(self):
        serializer = NurseSerializer()
        self.assertIn("user", serializer.get_fields())
        self.assertTrue(serializer.get_fields()["user"].read_only)
