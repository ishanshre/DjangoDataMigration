"""
Tests for Custom User Model
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ModelTests(TestCase):
    """
    Test Custom User Model
    """
    def test_create_user_with_username_successfull(self):
        """
        Testing create a new normal user with username is successfull.
        """
        email = "test@email.com"
        username = "testing"
        password = "testpass@123"
        full_name = "Admin User"
        phone_number = "9876543217"
        date_of_birth = timezone.now()
        user = User.objects.create_user(
            email=email,
            username=username,
            full_name=full_name,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            password=password
        )
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.full_name, full_name)
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.date_of_birth, date_of_birth)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser_with_username_successfull(self):
        """
        Testing create a new super user with username is successfull.
        """
        email = "test@email.com"
        username = "testing"
        password = "testpass@123"
        full_name = "Admin User"
        phone_number = "9876543217"
        date_of_birth = timezone.now()
        user = User.objects.create_superuser(
            email=email,
            username=username,
            full_name=full_name,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            password=password
        )
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.full_name, full_name)
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.date_of_birth, date_of_birth)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_new_user_email_normalized(self):
        """
        Test email is normalized in domain part
        """
        sample_emails = [
            ['test1','test1@EXAMPLE.com','test1@example.com'],
            ['test2','Test2@Example.COM','Test2@example.com'],
            ['test3','TEST3@EXAMPLE.COM','TEST3@example.com'],
            ['test4','test4@example.COM','test4@example.com'],
        ]
        password = "testpass@123"
        full_name = "Admin User"
        phone_number = "9876543217"
        date_of_birth = timezone.now()
        for username, email, expected in sample_emails:
            user = User.objects.create_superuser(
            email=email,
            username=username,
            full_name=full_name,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            password=password
            )
            self.assertEqual(user.email, expected)