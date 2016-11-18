from django.contrib.sitemaps import Sitemap
from mezzanine_agenda.models import Event
from organization.agenda.models import *
from organization.core.models import *
from organization.job.models import *
from organization.magazine.models import *
from organization.media.models import *
from organization.network.models import *
from organization.pages.models import *
from organization.projects.models import *
from organization.shop.models import *


class ArticleSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Article.objects.published()

    def lastmod(self, obj):
        return obj.publish_date


class PersonSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Person.objects.published()

    def lastmod(self, obj):
        return obj.publish_date


class ProjectSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Project.objects.published()

    def lastmod(self, obj):
        return obj.publish_date


class EventSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Event.objects.published()

    def lastmod(self, obj):
        return obj.publish_date


class PageSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Page.objects.published()

    def lastmod(self, obj):
        return obj.publish_date


class HomeSiteMap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return Home.objects.published()

    def lastmod(self, obj):
        return obj.publish_date


class PlaylistSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Playlist.objects.published()

    def lastmod(self, obj):
        return obj.publish_date
