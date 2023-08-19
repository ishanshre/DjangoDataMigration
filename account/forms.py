"""
This module contains forms related to User creation, change and authentication
"""

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for user registration (creation).

    This form inherits from Django's built-in UserCreationForm and customizes it
    for our User model.

    Fields:
    - username: The desired username for the user.
    - email: The user's email address.
    - full_name: The user's full name.
    - date_of_birth: The user's date of birth.
    - phone_number: The user's phone number.
    """
    class Meta(UserCreationForm.Meta):
        """
        It contains the meta data for user creaton form
        """
        model = User
        fields = ["username", "email", "full_name", "date_of_birth", "phone_number"]

class CustomUserChangeForm(UserChangeForm):
    """
    A custom form for user profile editing (change).

    This form inherits from Django's built-in UserChangeForm and customizes it
    for our User model.

    Fields:
    - username: The user's username.
    - email: The user's email address.
    - full_name: The user's full name.
    - date_of_birth: The user's date of birth.
    - phone_number: The user's phone number.
    """
    class Meta:
        """
        It contains the meta data for user change form
        """
        model = User
        fields = ["username","email", "full_name", "date_of_birth", "phone_number"]