from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Project


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    i18n = True
    alternates = True

    def items(self):
        return ["portfolio:home", "portfolio:project_list", "siteprofile:about", "contact:contact"]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    i18n = True
    alternates = True

    def items(self):
        return Project.objects.public()


sitemaps = {"static": StaticViewSitemap, "projects": ProjectSitemap}
