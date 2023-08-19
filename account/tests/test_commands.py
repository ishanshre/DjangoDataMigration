"""
Test custom management command in account app
"""
from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()

class TestPopulateFakeDataCommand(TestCase):
    """
    Test populate fake user data
    """
    def test_populate_fake_user(self):
        """
        Capture stdout to check the command's output
        """
        stdout = StringIO()
        total = 10
        # Call the management command with the desired number of fake users
        call_command('populate_fake_user', total, stdout=stdout)
        # Check if the expected message is in the command's output
        self.assertIn(
            f'Successfully populated the database with {total} fake users',
            stdout.getvalue()
        )
        # Check if the correct number of users were created
        self.assertEqual(User.objects.count(), total)

    def test_populate_fake_user_bulk(self):
        """
        Capture stdout to check the command's output
        """
        stdout = StringIO()
        total = 10
        # Call the management command with the desired number of fake users
        call_command('populate_fake_user_bulk', total, stdout=stdout)
        # Check if the expected message is in the command's output
        self.assertIn(
            f'Successfully populated the database with {total} fake users',
            stdout.getvalue()
        )
        # Check if the correct number of users were created
        self.assertEqual(User.objects.count(), total)
