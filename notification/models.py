from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Notification(models.Model):
    """
    Notification models stores user notification
    """
    message_body = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"notification {self.user.username}"