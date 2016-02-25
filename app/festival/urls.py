from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from festival.views import *

urlpatterns = patterns('',
    url(r'^artists/$', ArtistListView.as_view(), name="festival-artist-list"),
    url(r'^artists/(?P<pk>.*)/$', ArtistDetailView.as_view(), name="festival-artist-detail"),
    url(r'^videos/$', ArtistListView.as_view(), name="festival-video-list"),
    url(r'^videos/(?P<pk>.*)/$', ArtistDetailView.as_view(), name="festival-video-detail"),

)
