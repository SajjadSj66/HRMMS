from django.test import TestCase
from django.contrib.auth import get_user_model

class UserTestCase(TestCase):

    def test_create_user_with_default_role(self):
        """Test creating a user with default role (patient)."""
        user = get_user_model().objects.create_user(
            username='testuser',
            email='<EMAIL>',
            password='testpassword'
        )

        self.assertEqual(user.role, 'patient')
        self.assertTrue(user.username, 'testuser')
        self.assertEqual(user.email, '<EMAIL>')
        self.assertTrue(user.check_password('testpassword'))

    def test_create_user_with_specified_role(self):
        """Test creating a user with specified role (doctor)."""

        user = get_user_model().objects.create_user(
            username='doctoruser',
            email='<EMAIL>',
            password='testpassword',
            role='doctor'
        )

        self.assertEqual(user.role, 'doctor')
        self.assertTrue(user.username, 'doctoruser')
        self.assertEqual(user.email, '<EMAIL>')
        self.assertTrue(user.check_password('testpassword'))


    def test_create_superuser(self):
        """Test creating a superuser."""

        superuser = get_user_model().objects.create_superuser(
            username='adminuser',
            email='<EMAIL>',
            password='testpassword'
        )

        self.assertEqual(superuser.role, 'admin')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password('testpassword'))

    def test_str_method(self):
        """Test the __str__ method of the User model."""
        user = get_user_model().objects.create_user(
            username='testuser',
            email='<EMAIL>',
            password='testpassword'
        )
        self.assertEqual(str(user), 'testuser - <EMAIL> - testpassword')