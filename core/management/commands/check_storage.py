"""
Diagnose Supabase Storage uploads end to end.

    python manage.py check_storage

Uploads a tiny test file through whichever storage backend is active
(Supabase S3, or local disk if USE_SUPABASE_STORAGE=False), reads back
the URL Django generated for it, and — for Supabase — fetches that URL
over HTTP to confirm it actually returns the file instead of a 403 or
404. This catches the two most common causes of "images hazihifadhiwi":
a bucket name/region that doesn't match Supabase, and a public URL
that points at the wrong path (see the comment in settings.py above
AWS_S3_CUSTOM_DOMAIN for what that second one looks like).
"""
import urllib.request
import urllib.error

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Upload a test file to the configured storage backend and verify it is reachable.'

    def handle(self, *args, **options):
        using_supabase = getattr(settings, 'USE_SUPABASE_STORAGE', False)
        self.stdout.write(f"Backend: {'Supabase Storage (S3)' if using_supabase else 'Local filesystem'}")

        if using_supabase:
            self.stdout.write(f"  Bucket   : {settings.AWS_STORAGE_BUCKET_NAME}")
            self.stdout.write(f"  Region   : {settings.AWS_S3_REGION_NAME}")
            self.stdout.write(f"  Endpoint : {settings.AWS_S3_ENDPOINT_URL}")
            if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
                self.stderr.write(self.style.ERROR(
                    "  SUPABASE_S3_ACCESS_KEY / SUPABASE_S3_SECRET_KEY are missing or blank."
                ))
                return
            if not settings.AWS_S3_ENDPOINT_URL:
                self.stderr.write(self.style.ERROR("  SUPABASE_S3_ENDPOINT is missing or blank."))
                return

        test_name = 'check_storage/probe.txt'
        try:
            saved_name = default_storage.save(test_name, ContentFile(b'tryvis storage check'))
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"Upload FAILED: {exc}"))
            self.stderr.write(self.style.WARNING(
                "Common causes: wrong access key/secret, bucket name doesn't exist in "
                "Supabase, or SUPABASE_S3_REGION doesn't match the project's real region."
            ))
            return

        self.stdout.write(self.style.SUCCESS(f"Upload OK -> {saved_name}"))
        url = default_storage.url(saved_name)
        self.stdout.write(f"Generated URL: {url}")

        if using_supabase:
            try:
                with urllib.request.urlopen(url, timeout=10) as resp:
                    status = resp.status
            except urllib.error.HTTPError as e:
                status = e.code
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f"Could not reach the URL at all: {exc}"))
                default_storage.delete(saved_name)
                return

            if status == 200:
                self.stdout.write(self.style.SUCCESS("Fetch OK -> HTTP 200. Images will display correctly."))
            elif status == 403:
                self.stderr.write(self.style.ERROR(
                    "Fetch FAILED -> HTTP 403. The bucket is almost certainly set to Private. "
                    "Go to Supabase -> Storage -> your bucket -> Settings, and make it Public."
                ))
            elif status == 404:
                self.stderr.write(self.style.ERROR(
                    "Fetch FAILED -> HTTP 404. The public URL path is wrong for this project "
                    "(check AWS_S3_CUSTOM_DOMAIN in settings.py matches your Supabase project ref)."
                ))
            else:
                self.stderr.write(self.style.ERROR(f"Fetch FAILED -> HTTP {status}."))

        default_storage.delete(saved_name)
        self.stdout.write("(test file removed)")
