from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os

def home(request):
    return render(request, 'home.html')

def health_check(request):
    """Health check endpoint for monitoring and debugging."""
    return JsonResponse({
        'status': 'healthy',
        'debug': settings.DEBUG,
        'database_configured': bool(settings.DATABASES.get('default')),
        'allowed_hosts': settings.ALLOWED_HOSTS,
    })