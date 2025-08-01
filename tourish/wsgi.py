"""
WSGI config for Skillshare project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourish.settings')

# Setup Django
django.setup()

# Run migrations and collect static files automatically
try:
    call_command('migrate', interactive=False)
    call_command('collectstatic', interactive=False, verbosity=0)
except Exception as e:
    # Log the error or pass
    print(f"Error running migrations or collectstatic: {e}")

application = get_wsgi_application()
application = WhiteNoise(application)
