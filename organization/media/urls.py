# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from mezzanine.conf import settings

from organization.media.views import MediaDetailView, MediaOverlayView,\
    PlaylistDetailView, PlaylistListView, PlaylistOverlayView,\
    PlayListMediaView, LiveStreamingDetailView, DynamicMultimediaView
from organization.magazine.views import ArticleListRedirect

urlpatterns = []

if getattr(settings, 'DEACTIVATE_MEDIA_PAGES', False):
    urlpatterns += [
        url(
            "^medias/(?P<type>.*)/(?P<slug>.*)/detail/$",
            ArticleListRedirect.as_view(),
            name="organization_media-detail"
        ),
        url(
            "^playlists/(?P<slug>.*)/detail/$",
            ArticleListRedirect.as_view(),
            name="organization-playlist-detail"
        ),
        url(
            "^playlists/list/$",
            ArticleListRedirect.as_view(),
            name="organization-playlist-list"
        ),
        url(
            "^playlists/list/(?P<type>.*)/$",
            ArticleListRedirect.as_view(),
            name="organization-playlist-list"
        ),
    ]

urlpatterns += [
    url(
        "^medias/(?P<type>.*)/(?P<slug>.*)/detail/$",
        MediaDetailView.as_view(),
        name="organization_media-detail"
    ),
    url(
        "^medias/(?P<type>.*)/(?P<slug>.*)/overlay/$",
        MediaOverlayView.as_view(),
        name="organization_media-overlay"
    ),
    url(
        "^playlists/(?P<slug>.*)/detail/$",
        PlaylistDetailView.as_view(),
        name="organization-playlist-detail"
    ),
    url(
        "^playlists/list/$",
        PlaylistListView.as_view(),
        name="organization-playlist-list"
    ),
    url(
        "^playlists/list/(?P<type>.*)/$",
        PlaylistListView.as_view(),
        name="organization-playlist-list"
    ),
    url(
        "^playlists/overlay/(?P<slug>.*)/$",
        PlaylistOverlayView.as_view(),
        name="organization-playlist-overlay"
    ),
    url(
        "^playlist-media-autocomplete/$",
        permission_required('organization_media.change_playlist')(PlayListMediaView.as_view()),  # noqa: E501
        name='media-autocomplete'
    ),
    url(
        "^streams/(?P<slug>.*)/(?P<type>.*)/detail/$",
        LiveStreamingDetailView.as_view(),
        name="organization-streaming-detail"
    ),
    url(
        "^dynamic-multimedia/$",
        staff_member_required(DynamicMultimediaView.as_view()),
        name='dynamic-multimedia'
    ),
]
