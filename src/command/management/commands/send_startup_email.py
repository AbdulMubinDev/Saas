from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import os
import socket


class Command(BaseCommand):
    help = 'Send confirmation email when server starts up'

    def handle(self, *args, **options):
        # Get admin email from settings
        admin_email = getattr(settings, 'ADMIN_USER_EMAIL', None)

        if not admin_email:
            self.stdout.write(
                self.style.WARNING('No admin email configured. Set ADMIN_USER_EMAIL in environment variables.')
            )
            return

        # Get server information
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        # Get Railway-specific information if available
        railway_project_id = os.environ.get('RAILWAY_PROJECT_ID', 'N/A')
        railway_service_name = os.environ.get('RAILWAY_SERVICE_NAME', 'N/A')
        railway_environment = os.environ.get('RAILWAY_ENVIRONMENT', 'N/A')

        # Build email content
        subject = f'🚀 SaaS Server Started Successfully - {hostname}'

        message = f"""
Your SaaS Django application has started successfully!

Server Information:
- Hostname: {hostname}
- IP Address: {ip_address}
- Started at: {timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

Railway Deployment Info:
- Project ID: {railway_project_id}
- Service Name: {railway_service_name}
- Environment: {railway_environment}

Application Status:
✅ Database migrations completed
✅ Static files collected
✅ Server running on port {os.environ.get('PORT', '8000')}

You can access your application at:
- Main App: https://{hostname}
- Admin Panel: https://{hostname}/admin

This is an automated message sent when your server starts up.
"""

        try:
            # Send email
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[admin_email],
                fail_silently=False,
            )

            self.stdout.write(
                self.style.SUCCESS(f'Successfully sent startup confirmation email to {admin_email}')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to send startup email: {str(e)}')
            )
            # Don't raise the exception to avoid breaking server startup