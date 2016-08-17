from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from organization.magazine.views import *

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url("^article/$", ArticleListView.as_view(), name="magazine-article-list"),
    url("^article/detail/(?P<slug>.*)%s$" % _slash, ArticleDetailView.as_view(), name="magazine-article-detail"),
    url("^topic/detail/(?P<slug>.*)%s$" % _slash, TopicDetailView.as_view(), name='topic-detail'),
    url(
        r'^object-autocomplete/$',
        ObjectAutocomplete.as_view(),
        name='object-autocomplete',
    ),
]
