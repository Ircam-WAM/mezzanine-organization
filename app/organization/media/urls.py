from __future__ import unicode_literals

import django.views.i18n
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import permission_required

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from organization.media.views import *


urlpatterns = [
    url("^playlist/list/$", PlaylistListView.as_view(), name="organization-playlist-list"),
    url("^playlist/detail/(?P<slug>.*)/$", PlaylistDetailView.as_view(), name="organization-playlist-detail"),
    url("^playlist-media-autocomplete/$",  permission_required('playlist.can_edit')(PlayListMediaView.as_view()), name='media-autocomplete'),
    url("^media/detail/(?P<slug>.*)/$", MediaDetailView.as_view(), name="organization-media-detail"),
]
