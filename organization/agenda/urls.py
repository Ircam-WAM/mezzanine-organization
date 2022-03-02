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

from django.contrib.auth.decorators import permission_required
from django.conf.urls import include, url

from mezzanine.conf import settings

from organization.agenda.views import DynamicContentEventView, EventDetailView

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url(
        "^%s/(?P<slug>.*)/detail%s$" % (settings.EVENT_SLUG, _slash),
        EventDetailView.as_view(),
        name='event_detail'
    ),
    url(
        "^%s[%s]?" % (settings.EVENT_SLUG, _slash),
        include("mezzanine_agenda.urls")
    ),
    url(
        "^dynamic-content-event/$",
        permission_required('mezzanine_agenda.change_event')(DynamicContentEventView.as_view()),  # noqa: E501
        name='dynamic-content-event'
    ),
]
