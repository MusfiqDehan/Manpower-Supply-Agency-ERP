import os
from .base import *
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://manpower-supply-agency.musfiqdehan.com",
    "https://manpower-supply-agency.up.railway.app",
]

DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# SECURE_SSL_REDIRECT = True

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("DB_NAME"),
#         "USER": os.getenv("DB_USER"),
#         "PASSWORD": os.getenv("DB_PASSWORD"),
#         "HOST": os.getenv("DB_HOST"),
#         "PORT": os.getenv("DB_PORT"),
#     },
# }

# dj_database_url settings
DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"), conn_max_age=600, ssl_require=True),
}


# AWS s3 bucket settings
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", default=None)
AWS_LOCATION = os.getenv("AWS_LOCATION", default=None)
AWS_S3_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID", default=None)
AWS_S3_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY", default=None)
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN", default=None)
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL", default=None)
AWS_S3_FILE_OVERWRITE = os.getenv("AWS_S3_FILE_OVERWRITE", default=None)

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR.parent / "staticfiles"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.parent / "mediafiles"

# Production Storage Settings
if AWS_STORAGE_BUCKET_NAME:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "LOCATION": f"{AWS_LOCATION}/staticfiles",
        },
        "mediafiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "LOCATION": f"{AWS_LOCATION}/mediafiles",
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
        "mediafiles": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "LOCATION": MEDIA_ROOT,
        },
    }


# Celery Settings
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", default=None)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", default=None)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Dhaka"

# Email Settings
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", default=None)
EMAIL_HOST = os.getenv("EMAIL_HOST", default=None)
EMAIL_PORT = os.getenv("EMAIL_PORT", default=None)
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", default=None)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", default=None)
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", default=None)
