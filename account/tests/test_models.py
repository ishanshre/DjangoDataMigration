"""
Tests for Custom User Model
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from account.models import Profile

User = get_user_model()

class ModelTests(TestCase):
    """
    Test Custom User Model
    """

    def setUp(self):
        self.email = "test@email.com"
        self.username = "testing"
        self.password = "testpass@123"
        self.full_name = "Admin User"
        self.phone_number = "+9779842586931"
        self.date_of_birth = timezone.now()
        self.user = User.objects.create_user(
            email=self.email,
            username=self.username,
            full_name=self.full_name,
            date_of_birth=self.date_of_birth,
            phone_number=self.phone_number,
            password=self.password
        )
        
    def test_create_user_with_username_successfull(self):
        """
        Testing create a new normal user with username is successfull.
        """
        
        
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.full_name, self.full_name)
        self.assertEqual(self.user.phone_number, self.phone_number)
        self.assertEqual(self.user.date_of_birth, self.date_of_birth)
        self.assertTrue(self.user.check_password(self.password))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
    
    def test_create_superuser_with_username_successfull(self):
        """
        Testing create a new super user with username is successfull.
        """
        username = "admin"
        email = "admin@admin.com"
        full_name="Admin User"
        user = User.objects.create_superuser(
            email=email,
            username=username,
            full_name=full_name,
            date_of_birth=self.date_of_birth,
            phone_number=self.phone_number,
            password=self.password
        )
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.full_name, self.full_name)
        self.assertEqual(user.phone_number, self.phone_number)
        self.assertEqual(user.date_of_birth, self.date_of_birth)
        self.assertTrue(user.check_password(self.password))
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
        phone_number = "+9779842586931"
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
    
    def test_auto_profile_created(self):
        profile = Profile.objects.get(user=self.user)
        self.assertIsInstance(profile, Profile)
        self.assertEqual(self.user.username, profile.user.username)