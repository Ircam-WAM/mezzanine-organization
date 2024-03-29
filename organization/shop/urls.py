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

from mezzanine.conf import settings

from organization.shop.views import CustomProductDetailView

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url(
        "^shop/",
        include("cartridge.shop.urls")
    ),
    url(
        "^product/(?P<slug>.*)%s$" % _slash,
        CustomProductDetailView.as_view(),
        name="custom_shop_product"
    ),
]
