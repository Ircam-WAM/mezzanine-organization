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

from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.admin import *

from organization.core.admin import *
from organization.projects.models import *
from organization.pages.models import *
from organization.shop.models import *
from organization.shop.translation import *
from cartridge.shop.admin import *


class ProductListProductInline(TabularDynamicInlineAdmin):

    model = ProductListProduct


class ProductListAdmin(BaseTranslationOrderedModelAdmin):

    inlines = [ProductListProductInline, ]
    first_fields = ['title', 'description',]


class ProductLinkInline(TabularDynamicInlineAdmin):

    model = ProductLink

class ProductPrestashopProductInline(TabularDynamicInlineAdmin):

    model = ProductPrestashopProduct


class CustomProductAdmin(ProductAdmin):

    inlines = [ProductImageAdmin, ProductVariationAdmin, ProductLinkInline,
                ProductPrestashopProductInline]


admin.site.register(ProductList, ProductListAdmin)
admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
