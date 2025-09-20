from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def health_check(request):
    """Health check endpoint for monitoring and debugging."""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'environment': os.environ.get('RAILWAY_ENVIRONMENT', 'development'),
        'hostname': os.environ.get('HOSTNAME', 'unknown'),
        'debug': settings.DEBUG,
        'database_configured': bool(settings.DATABASES.get('default')),
        'email_configured': bool(
            getattr(settings, 'EMAIL_HOST', None) and
            getattr(settings, 'EMAIL_HOST_USER', None)
        ),
    })