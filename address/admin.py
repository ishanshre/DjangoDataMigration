from django.contrib import admin

from address.models import Address
# Register your models here.

# Register Model to display in admin pannel
admin.site.register(Address)
