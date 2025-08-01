from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country_name = models.TextField(blank=True, null=True)
    phone_number = models.TextField()
    location = models.TextField(blank=True,null=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.jpg')
    id_photo = models.ImageField(upload_to='document_images/',blank=True)

    def __str__(self):
        return self.user.username
    


class EmergencyAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    country_name = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.jpg')
    id_photo = models.ImageField(upload_to='document_images/', null=True)

    def __str__(self):
        return f"Emergency by {self.user.username} at {self.timestamp}"
    