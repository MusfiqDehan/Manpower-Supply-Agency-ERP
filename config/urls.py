from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from .mysitemap import MySitemap


sitemaps = {"pages": MySitemap}

urlpatterns = [
    # Administration Default Dashboard
    path("r-admin/", admin.site.urls),
    # Website v2 Home page.
    path("", include("website_v2.urls")),
    # ERP Dashboard
    path("erp/", include("dashboard_app.urls")),
    # Administration app urls(Account and Permissions Management)
    path("administration/", include("administration_app.urls")),
    # Agent Management
    path("agent/", include("agent_management_app.urls")),
    # Passenger and Passport Management
    path("passenger/", include("passenger_app.urls")),
    # Visa Management
    path("visa/", include("visa_management_app.urls")),
    # Company Documents Management
    path("company-documents/", include("company_documentation_app.urls")),
    # company cost Management app
    path("company-cost/", include("company_cost_app.urls")),
    # Sitemap and robots.txt For SEO
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]


# If in development mode, add the static and media files to the urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
