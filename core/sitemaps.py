from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from projects.models import Project


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return ['core:home', 'projects:list', 'core:legal']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == 'core:home' else 0.8


class ProjectSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.6

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('projects:detail', args=[obj.pk])
