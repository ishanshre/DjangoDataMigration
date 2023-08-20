"""
    This module is management commands for populating fake user data in bulk
"""
from faker import Faker

from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    """
    Custom management command to populate fake user data

    Usuage:
        python manage.py populate_fake_user <total>
    
    Args:
        total (int): total numbers of fake data
    
    Example:
        To create 1000 fake users, run:
            python manage.py populate_fake_user 1000
    """
    help = "Populate the database with fake user data"

    def add_arguments(self, parser):
        """
        Define command-line arguments for the management command.

        Args:
            parser (ArgumentParser): The argument parser.
        """
        parser.add_argument("total", type=int, help="total: total number of fake user data")
    
    def handle(self, *args, **kwargs):
        """
        Handle the execution logic of the management commmand

        Args:
            args: Additional Arguments.
            kwargs: Additional keyword arguments
        """
        total = kwargs["total"]
        fake = Faker()

        unique_usernames = set()
        # Create a list to hold the fake user objects
        users = []
        for _ in range(total):
            fake_email = fake.email()
            fake_username = self.generate_unique_username(fake, unique_usernames)
            fake_full_name = fake.name()
            fake_date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
            fake_phone_number = fake.phone_number()
            fake_password = "Password@123"
            user = User.objects.create_user(
                email=fake_email,
                username=fake_username,
                full_name=fake_full_name,
                date_of_birth=fake_date_of_birth,
                phone_number=fake_phone_number,
            )
            user.set_password(fake_password)
            users.append(user)
        User.objects.bulk_create(users, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {total} fake users'))

    def generate_unique_username(self, fake, unique_usernames):
        """
        Generate a unique username.

        Args:
            fake (Faker): The Faker instance.
            unique_usernames (set): A set of unique usernames.

        Returns:
            str: A unique username.
        """

        while True:
            fake_username = fake.user_name()
            if fake_username not in unique_usernames:
                unique_usernames.add(fake_username)
                return fake_username
            