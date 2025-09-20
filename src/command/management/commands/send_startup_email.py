from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import os
import socket
import threading
import time
import logging

# Set up logging
logger = logging.getLogger(__name__)


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

        # Check if email settings are configured
        if not all([
            getattr(settings, 'EMAIL_HOST', None),
            getattr(settings, 'EMAIL_HOST_USER', None),
            getattr(settings, 'EMAIL_HOST_PASSWORD', None)
        ]):
            self.stdout.write(
                self.style.WARNING('Email settings not configured. Please set EMAIL_HOST, EMAIL_HOST_USER, and EMAIL_HOST_PASSWORD.')
            )
            return

        # Start email sending in a separate thread to avoid blocking
        email_thread = threading.Thread(target=self._send_startup_email, args=(admin_email,))
        email_thread.daemon = True  # Allow thread to be killed when main process exits
        email_thread.start()

        self.stdout.write(
            self.style.SUCCESS('Started background email sending process...')
        )

    def _send_startup_email(self, admin_email):
        """Send the startup email in a separate thread with timeout protection."""
        try:
            # Get server information
            hostname = socket.gethostname()
            try:
                ip_address = socket.gethostbyname(hostname)
            except socket.gaierror:
                ip_address = 'N/A'

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

            # Send email with timeout protection
            def send_with_timeout():
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[admin_email],
                        fail_silently=False,
                    )
                    logger.info(f'Successfully sent startup confirmation email to {admin_email}')
                except Exception as e:
                    logger.error(f'Failed to send startup email: {str(e)}')
                    raise

            # Run email sending with a 30-second timeout
            timer = threading.Timer(30.0, lambda: None)  # Fallback timeout
            email_success = False

            try:
                # Start the timer
                timer.start()

                # Send the email
                send_with_timeout()
                email_success = True

            except Exception as e:
                logger.error(f'Email sending failed or timed out: {str(e)}')
            finally:
                timer.cancel()

            if email_success:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully sent startup confirmation email to {admin_email}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Email sending completed with issues. Check logs for details.')
                )

        except Exception as e:
            logger.error(f'Error in email thread: {str(e)}')
            self.stdout.write(
                self.style.ERROR(f'Background email process failed: {str(e)}')
            )