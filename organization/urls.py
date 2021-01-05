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

import django.views.i18n
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

admin.autodiscover()

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from django.views.generic.base import RedirectView

from .ircam_oauth2_provider.views import serverLogout
urlpatterns = []

if "drum.links" in settings.INSTALLED_APPS:
    urlpatterns += [
        url("^%s/" % settings.DRUM_SLUG, include("drum.links.urls")),
    ]

urlpatterns += [
    url("^", include('organization.core.urls')),
    url("^", include('organization.pages.urls')),
    url("^", include('organization.magazine.urls')),
    url("^", include('organization.media.urls')),
    url("^", include('organization.projects.urls')),
    url("^", include('organization.network.urls')),
    url("^", include('organization.agenda.urls')),
    url("^", include('organization.job.urls')),
    url("^", include('organization.shop.urls')),
]

if settings.DEBUG :
    urlpatterns += [
        url(r'^hijack/', include('hijack.urls')),
    ]

# Mezzanine's Accounts app
# # we prefer oauth2
if settings.OAUTH2_IRCAM:
    urlpatterns += [
    url(r'^accounts/signup/$', RedirectView.as_view(url=settings.OAUTH_SIGNUP_URL, permanent=False, query_string=True), name="account_signup"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^serverlogout/',serverLogout)
    #url(r'^accounts/profile$', views.ProfileView),
    ]
else:
    urlpatterns += [
    url(r'^serverlogout/',RedirectView.as_view(url=settings.LOGOUT_URL, permanent=False, query_string=True), name="account_logout"),
    ]