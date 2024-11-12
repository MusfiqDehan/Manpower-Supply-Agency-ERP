import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", default=None)

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # For Generating Sitemaps
    "django.contrib.sitemaps",
    # For custom attributes
    "utils",
    # Dashboard app
    "dashboard_app",
    # Administration App
    "administration_app",
    # Agent App
    "agent_management_app",
    # Passenger App
    "passenger_app",
    # Visa Management
    "visa_management_app",
    # Website Version-2 App
    "website_v2",
    # Company Documentation app
    "company_documentation_app",
    # Company Cost Management app
    "company_cost_app",
    # 3rd Party Apps
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "manpower_supply_agency_erp.urls"

WSGI_APPLICATION = "manpower_supply_agency_erp.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    # {
    #     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]

# custom user model is properly configured
AUTH_USER_MODEL = "administration_app.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_UNIQUE_EMAIL = True

LOGIN_REDIRECT_URL = "index:dashboard"
# ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login'

LOGIN_URL = "/administration/login/"
LOGOUT_REDIRECT_URL = "/administration/login/"

# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Dhaka"

USE_I18N = True

USE_TZ = True


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.parent / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Custom context processors
                "utils.context_processors.notifications_processor",
            ],
        },
    },
]


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Custom Error handler
handler403 = "website_v2.views.custom_403"
handler404 = "website_v2.views.custom_404"
