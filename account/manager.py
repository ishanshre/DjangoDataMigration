"""
This module contains the custom managers for models in this app.
"""

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom manager for User Model
    """

    def __create_user(
            self,
            email,
            username,
            full_name,
            password=None,
            **kwargs):
        """
        Create and return a user with the given attributes.

        Args:
            email (str): The user email address
            username (str): The user's username.
            full_name (str): The user's full name.
            password (str, optional): The user's password.
        
        Returns:
            A user instance

        Raises
            ValueError: If email is not provided.
        """
        # check if email is provided
        if not email:
            raise ValueError("The email must be set")       
        # normalize the email domain part to lowercase
        email = self.normalize_email(email)

        # new user instance
        user = self.model(email=email, username=username, full_name=full_name, **kwargs)

        # set the user password (if provided) and save to database
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, full_name, password=None, **kwargs):
        """
        Create a normal user with given attributes

        Args:
            email (str): The user email address
            username (str): The user's username.
            full_name (str): The user's full name.
            password (str, optional): The user's password.
        
        Returns:
            A user instance
            
        Raises
            ValueError: If is_staff or is_superuser is set to true

        """
        # Ensure is_staff and is_superuser to False
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        # check that is_staff and is_superuser are not set to True for normal user
        if kwargs.get("is_staff") is not False:
            raise ValueError("Normal user must set is_staff=False")
        if kwargs.get("is_superuser") is not False:
            raise ValueError("Normal user must set is_superuser=False")
        # create a user using the private __create_user method.
        return self.__create_user(email, username, full_name, password, **kwargs)

    def create_superuser(self, email, username, full_name, password=None, **kwargs):
        """
        Create a super user with given attributes

        Args:
            email (str): The user email address
            username (str): The user's username.
            full_name (str): The user's full name.
            password (str, optional): The user's password.
        
        Returns:
            A user instance
            
        Raises
            ValueError: If is_staff or is_superuser is set to true

        """
        # Ensure is_staff and is_superuser to True
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
         # check that is_staff and is_superuser are not set to False for super user
        if kwargs.get('is_staff') is not True:
            raise ValueError("Superuser must set is_staff=True")
        if kwargs.get('is_superuser') is not True:
            raise ValueError("Superuser must set is_superuser=True")
        # create a super user using the private __create_user method.
        return self.__create_user(email, username, full_name, password, **kwargs)