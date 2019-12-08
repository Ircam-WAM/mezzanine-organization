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

from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings
from organization.pages.views import *

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url("^$", HomeView.as_view(), name="home"),
    url("^dynamic-content-home-slider/$", permission_required('organization-pages.change_home')(DynamicContentHomeSliderView.as_view()), name='dynamic-content-home-slider'),
    url("^dynamic-content-home-body/$",  permission_required('organization-pages.change_home')(DynamicContentHomeBodyView.as_view()), name='dynamic-content-home-body'),
    url("^dynamic-content-home-media/$",  permission_required('organization-pages.change_home')(DynamicContentHomeMediaView.as_view()), name='dynamic-content-home-media'),
    url("^dynamic-content-page/$",  permission_required('organization-pages.change_custompage')(DynamicContentPageView.as_view()), name='dynamic-content-page'),
    url("^home/$", HomeView.as_view(), name='organization-home'),
    url("^newsletter/$", NewsletterView.as_view(), name='organization-newsletter'),
    url("^information/$", InformationView.as_view(), name='organization-information'),
    url("^publications/$", PublicationsView.as_view(), name='publications'),

]
