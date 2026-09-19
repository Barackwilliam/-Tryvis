"""
Django settings for Tryvis Investments Limited website.
Database: Supabase Postgres. Media: Supabase Storage bucket (S3-compatible).
"""
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-env')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.company_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------------------------------------------------------------------
# Database — Supabase Postgres
# Get this connection string from: Supabase project > Settings > Database
# Use the "Connection pooling" URI (port 6543) in production.
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='postgres'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default='6543'),
        'OPTIONS': {'sslmode': 'require'},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Dar_es_Salaam'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ---------------------------------------------------------------------------
# Media — Supabase Storage bucket, accessed via its S3-compatible API
# Get these from: Supabase project > Settings > Storage > S3 Connection
# ---------------------------------------------------------------------------
USE_SUPABASE_STORAGE = config('USE_SUPABASE_STORAGE', default=True, cast=bool)

if USE_SUPABASE_STORAGE:
    AWS_ACCESS_KEY_ID = config('SUPABASE_S3_ACCESS_KEY', default='')
    AWS_SECRET_ACCESS_KEY = config('SUPABASE_S3_SECRET_KEY', default='')
    AWS_STORAGE_BUCKET_NAME = config('SUPABASE_BUCKET_NAME', default='tryvis-media')
    AWS_S3_ENDPOINT_URL = config('SUPABASE_S3_ENDPOINT', default='')  # e.g. https://<project-ref>.supabase.co/storage/v1/s3
    AWS_S3_REGION_NAME = config('SUPABASE_S3_REGION', default='eu-central-1')
    AWS_S3_ADDRESSING_STYLE = 'path'
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
    STORAGES = {
        'default': {'BACKEND': 'storages.backends.s3.S3Storage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
    }

    # ------------------------------------------------------------------
    # IMPORTANT — read this if uploaded images don't show up on the site.
    #
    # django-storages does NOT use MEDIA_URL to build a file's .url —
    # it builds its own URL from AWS_S3_ENDPOINT_URL. Supabase's S3
    # *API* endpoint ("/storage/v1/s3") is a different path to its
    # *public file* URL ("/storage/v1/object/public/<bucket>/<file>").
    # Without AWS_S3_CUSTOM_DOMAIN telling it which one to use for
    # links, django-storages links to the API path, which returns 403
    # in a browser. The upload itself succeeds either way — the file
    # really is in the bucket — the <img> link is just wrong, so the
    # image looks like it "didn't save".
    #
    # This derives the correct public path automatically from
    # SUPABASE_S3_ENDPOINT, so nothing extra needs to be set in .env.
    # It also requires the bucket to be marked Public in the Supabase
    # dashboard (Storage → your bucket → Settings) — a private bucket
    # returns 403 on this URL no matter how it's built.
    # ------------------------------------------------------------------
    _supabase_project_url = AWS_S3_ENDPOINT_URL.removesuffix('/storage/v1/s3').removesuffix('/storage/v1/s3/')
    AWS_S3_CUSTOM_DOMAIN = f'{_supabase_project_url.split("://", 1)[-1]}/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}'
    MEDIA_URL = f'{_supabase_project_url}/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}/'
else:
    STORAGES = {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
    }
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#database botikawilly@gmail.com
#hosting jafarikilindo@gmail.com
