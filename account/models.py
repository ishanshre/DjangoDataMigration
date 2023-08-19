"""
This module contains database models for account app
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Import custom user manager
from account.manager import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for the application.

    This model represents a user account in the system.

    Attributes:
        email (EmailField): The user's email address.
        username (CharField): The user's unique username.
        full_name (CharField): The user's full name.
        date_of_birth (DateField): The user's date of birth.
        phone_number (CharField): The user's phone number.
        is_active (BooleanField): Indicates if the user account is active.
        is_staff (BooleanField): Indicates if the user has staff permissions.

    Methods:
        __str__: Returns the username as a string representation of the user.

    Usage:
        This model is used for managing user accounts in the application.
    """
    email: models.EmailField = models.EmailField(max_length=255)
    username: models.CharField = models.CharField(max_length=255, unique=True)
    full_name: models.CharField = models.CharField(max_length=255)
    date_of_birth: models.DateField = models.DateField()
    phone_number: models.CharField = models.CharField(max_length=10)
    is_active: models.BooleanField = models.BooleanField(default=True)
    is_staff: models.BooleanField = models.BooleanField(default=False)

    # Define the custom user manager
    objects: CustomUserManager = CustomUserManager()

    # Define the field to use as the username for authentication
    USERNAME_FIELD: str = 'username'

    # Define the required fields to use as the username when authenticating
    REQUIRED_FIELDS: list = ['email', 'full_name', 'date_of_birth', 'phone_number']

    def __str__(self) -> str:
        """
        Return the username as a string representation of the user.

        Returns:
            str: The username of the user.
        """
        return f"{self.username}"
