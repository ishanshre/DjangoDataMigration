"""
This module contains database models for account app
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission

# third party import
from phonenumber_field.modelfields import PhoneNumberField

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
    phone_number: models.CharField = models.CharField(max_length=15)
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


class NewUser(AbstractBaseUser, PermissionsMixin):
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
        joined_at (DateTimeField): Indicates the timestamp when user registers.
        updated_at (DateTimeField): Indicates the timestamp when user performs an update.

    Methods:
        __str__: Returns the username as a string representation of the user.

    Usage:
        This model is used for managing user accounts in the application.
    """
    email: models.EmailField = models.EmailField(max_length=255, unique=True, db_index=True)
    username: models.CharField = models.CharField(max_length=255, unique=True, db_index=True)
    full_name: models.CharField = models.CharField(max_length=255)
    date_of_birth: models.DateField = models.DateField(db_index=True)
    phone_number: models.CharField = PhoneNumberField(region="NP")
    is_active: models.BooleanField = models.BooleanField(default=True)
    is_staff: models.BooleanField = models.BooleanField(default=False)
    joined_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name="NewUser_set",
        blank=True,
        verbose_name="groups",
        help_text='''The groups this user belongs to. 
                User will get permissions granted to each of their groups.''',
     )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='NewUser_set',  # Use a unique related_name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

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


class Profile(models.Model):
    """
    Profile table has one to one relationship with new users table.
    Add additional user info.
    """
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=10000, null=True, blank=True)
    avatar = models.ImageField(upload_to="user/profile/avatar", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a string
        """
        return f"{self.user.username}"


class Activity(models.Model):
    """
    Activity store the user's activity like login, update, and so on
    """
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name="activities")
    activity_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.user.username
