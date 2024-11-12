from .base import *
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from the .env file

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "db.sqlite3",
    }
}

# Static settings for development
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR.parent / "static"]
STATIC_ROOT = BASE_DIR.parent / "staticfiles/static"

# Media settings for development
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.parent / "mediafiles/media"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        "LOCATION": STATIC_ROOT,
    },
    "mediafiles": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "LOCATION": MEDIA_ROOT,
    },
}
