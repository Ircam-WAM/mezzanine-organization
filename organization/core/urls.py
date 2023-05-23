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


from django.conf.urls import include, url

from rest_framework import routers

from mezzanine.conf import settings

from .views import CustomSearchView, UserProjectsView,\
     UserProducerView, MetaCategoryViewSet


LOGIN_URL = settings.LOGIN_URL
_slash = "/" if settings.APPEND_SLASH else ""


router = routers.SimpleRouter()

router.register(
    r"categories",
    MetaCategoryViewSet,
    basename="api-meta-categories",
)

urlpatterns = [
    url("^search/$", CustomSearchView.as_view(), name="search"),
    url("^profile/projects/$", UserProjectsView.as_view(), name="user_projects"),
    url("^profile/producer/$", UserProducerView.as_view(), name="user_producer"),
]
