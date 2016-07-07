from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from organization.magazine.views import *


urlpatterns = [
    url(r'^article/$', ArticleListView.as_view(), name="magazine-article-list"),
    url(r'^article/detail/(?P<slug>.*)/$', ArticleDetailView.as_view(), name="magazine-article-detail"),
]
