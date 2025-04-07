import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from users.serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, ChangePasswordSerializer
)

User = get_user_model()


@pytest.mark.django_db
class TestUserSerializers:

    def test_user_serializer_fields(self):
        user = User.objects.create_user(username="tester", email="t@test.com", password="pass1234", role="patient")
        serializer = UserSerializer(user)
        assert serializer.data["username"] == "tester"
        assert serializer.data["email"] == "t@test.com"
        assert "password" in serializer.fields

    def test_register_serializer_creates_user(self):
        data = {
            "username": "newuser",
            "email": "new@user.com",
            "password": "StrongPass123!",
            "role": "patient"
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert User.objects.filter(username="newuser").exists()
        assert user.email == "new@user.com"

    def test_register_serializer_invalid_password(self):
        data = {
            "username": "baduser",
            "email": "bad@user.com",
            "password": "123",  # Too short / weak
            "role": "doctor"
        }
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_login_serializer_valid_credentials(self):
        user = User.objects.create_user(username="logintest", password="TestPass123")
        data = {"username": "logintest", "password": "TestPass123"}
        serializer = LoginSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        tokens = serializer.validated_data
        assert "access" in tokens
        assert "refresh" in tokens
        assert tokens["user"]["username"] == "logintest"

    def test_login_serializer_invalid_credentials(self):
        data = {"username": "wrong", "password": "wrongpass"}
        serializer = LoginSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_change_password_serializer_valid(self, rf):
        user = User.objects.create_user(username="changepass", password="OldPass123")
        request = rf.post("/change-password/")
        request.user = user

        serializer = ChangePasswordSerializer(
            data={"old_password": "OldPass123", "new_password": "NewPass456!"},
            context={"request": request}
        )
        assert serializer.is_valid(), serializer.errors
        serializer.update(user, serializer.validated_data)
        assert user.check_password("NewPass456!")

    def test_change_password_serializer_invalid_old_password(self, rf):
        user = User.objects.create_user(username="changepass", password="CorrectOld123")
        request = rf.post("/change-password/")
        request.user = user

        serializer = ChangePasswordSerializer(
            data={"old_password": "WrongOld", "new_password": "NewPass456!"},
            context={"request": request}
        )
        assert not serializer.is_valid()
        assert "old_password" in serializer.errors
