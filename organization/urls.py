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
    url("^festival/", include('organization.festival.urls')),
    url("^magazine/", include('organization.magazine.urls')),
    url("^media/", include('organization.media.urls')),
    url("^project/", include('organization.project.urls')),
    url("^team/", include('organization.team.urls')),
]
