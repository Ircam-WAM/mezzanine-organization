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
from mezzanine.conf import settings

from organization.magazine.views import MagazineDetailView, ArticleDetailView,\
    ArticleListView, TopicDetailView, ObjectAutocomplete,\
    DynamicContentMagazineContentView, DynamicContentArticleView, ArticleEventView,\
    ArticleEventTeamView

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url(
        "^article/detail/(?P<slug>.*)[%s]$" % _slash,
        ArticleDetailView.as_view(),
        name="magazine-article-detail"
    ),
    url(
        "^article/list[%s]?$" % _slash,
        ArticleListView.as_view(),
        name="magazine-article-list"
    ),
    url(
        "^article/list/(?P<keyword>.*)[%s]$" % _slash, ArticleListView.as_view(),
        name="magazine-article-list"
    ),
    url(
        "^topic/detail/(?P<slug>.*)[%s]$" % _slash,
        TopicDetailView.as_view(),
        name='topic-detail'
    ),
    url(
        "^object-autocomplete/$",
        ObjectAutocomplete.as_view(),
        name='object-autocomplete'
    ),
    url(
        "^dynamic-content-article[/]?$",
        DynamicContentArticleView.as_view(),
        name='dynamic-content-article'
    ),
    url(
        "^article-event-list[/]?$",
        ArticleEventView.as_view(),
        name='article-event-list'
    ),
    url(
        '^team/(?P<slug>.*)/article-event-list[/]?$',
        ArticleEventTeamView.as_view(),
        name='article-event-team-list'
    ),
    url(
        "^dynamic-content-magazine/$",
        permission_required('organization_magazine.change_magazine')(DynamicContentMagazineContentView.as_view()),  # noqa: E501
        name='dynamic-content-magazine'
    ),
    url(
        "^magazine[/]?$",
        MagazineDetailView.as_view(),
        name='magazine'
    ),
]
