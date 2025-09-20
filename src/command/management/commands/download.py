import helpers
from typing import Any
from django.core.management.base import BaseCommand
from django.conf import settings

VENDOR_STATICFILES = {
    "flowbite.min.css": "https://cdn.jsdelivr.net/npm/flowbite@3.1.2/dist/flowbite.min.css" ,
    "flowbite.min.js": "https://cdn.jsdelivr.net/npm/flowbite@3.1.2/dist/flowbite.min.js" ,
}

STATICFILES_VENDOR_DIR = getattr(settings, 'STATICFILES_VENDOR_DIR')

class Command(BaseCommand):
    help = "Download vendor static files like CSS and JavaScript libraries"

    def handle(self, *args:Any, **options:Any):
        completed_url = []
        for name, url in VENDOR_STATICFILES.items():
            out_path = STATICFILES_VENDOR_DIR / name
            dl_success = helpers.cdn_downloader(url, out_path)
            if dl_success:
                completed_url.append(url)
            else:
                self.stdout.write(
                    self.style.ERROR(f"[-]Failed to download {url}")
                )
        if set(completed_url) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(
                self.style.SUCCESS(f"[+]Successfully updated vendors static files")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"[-]Some files are not updated")
            )