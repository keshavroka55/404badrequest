from django.contrib import admin
from .models import UserProfile,EmergencyAlert
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(EmergencyAlert)
