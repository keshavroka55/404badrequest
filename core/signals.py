from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from .models import EmergencyAlert, UserProfile
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import os


@receiver(post_save, sender= User)
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



@receiver(post_save, sender=EmergencyAlert)
def send_emergency_email(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        profile = user.userprofile
        subject = f"🚨 EMERGENCY ALERT: {user.username}"

        # HTML email content using template
        html_message = render_to_string('complain/emergency_alert.html', {
            'user': user,
            'profile': profile,
            'latitude': instance.latitude,
            'longitude': instance.longitude,
            'timestamp': instance.timestamp,
            'maps_link': f"https://www.google.com/maps?q={instance.latitude},{instance.longitude}"
        })

        email = EmailMessage(
            subject,
            body=html_message,
            from_email='krishjak1244@gmail.com', 
            to=['keshavrokaya1244@gmail.com'],
        )
        email.content_subtype = 'html'

        # Attach profile image and ID photo
        if profile.profile_image:
            email.attach_file(profile.profile_image.path)
        if profile.id_photo:
            email.attach_file(profile.id_photo.path)

        email.send()

        
