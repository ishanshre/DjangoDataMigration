"""
Admin pannel config for this app.
"""
from django.contrib import admin

from notification.models import Notification

# Register Model to display in admin pannel
admin.site.register(Notification)
