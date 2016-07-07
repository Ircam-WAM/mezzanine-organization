from __future__ import unicode_literals

import django.views.i18n
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from organization.media.views import *


urlpatterns = [
    url(r'^videos/$', VideoListView.as_view(), name="festival-video-list"),
    url(r'^videos/detail/(?P<slug>.*)/$', VideoDetailView.as_view(), name="festival-video-detail"),
    url(r'^videos/category/(?P<slug>.*)/$', VideoListCategoryView.as_view(), name="festival-video-list-category"),
]
