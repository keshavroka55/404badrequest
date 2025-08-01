

from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    date_submitted = models.DateTimeField(auto_now_add=True)
    action_taken = models.BooleanField(default=False)
    action_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject}"

