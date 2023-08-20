from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Address(models.Model):
    """
    Address model stores user address informations.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses"
    )
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.street_address}"
