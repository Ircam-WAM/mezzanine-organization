from __future__ import unicode_literals

import django.views.i18n
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

admin.autodiscover()

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings


urlpatterns = [
    url("^", include('organization.core.urls')),
    url("^", include('organization.pages.urls')),
    url("^", include('organization.featured.urls')),
    url("^", include('organization.festival.urls')),
    url("^", include('organization.magazine.urls')),
    url("^", include('organization.media.urls')),
    url("^", include('organization.project.urls')),
    url("^", include('organization.team.urls')),
]
