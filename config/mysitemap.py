from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class MySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return [
            "website_v2:home",
            "website_v2:about",
            "website_v2:services",
            "website_v2:countries",
            "website_v2:career",
            "website_v2:contact",
        ]

    def location(self, item):
        return reverse(item)

    # def lastmod(self, obj):
    #     return obj.updated_at  # Replace with your model's last modified field
