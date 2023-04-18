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


from django.contrib import admin

from mezzanine.core.admin import TabularDynamicInlineAdmin, BaseTranslationModelAdmin

from organization.core.admin import BaseTranslationOrderedModelAdmin
from organization.shop.models import ProductListProduct, ProductLink,\
    ProductExternalShop, TeamProduct, Product, ProductKeyword, ProductList
from cartridge.shop.admin import ProductAdmin, ProductImageAdmin,\
    ProductVariationAdmin


class ProductListProductInline(TabularDynamicInlineAdmin):

    model = ProductListProduct


class ProductListAdmin(BaseTranslationOrderedModelAdmin):

    inlines = [ProductListProductInline, ]
    first_fields = ['title', 'description', ]


class ProductLinkInline(TabularDynamicInlineAdmin):

    model = ProductLink


class ProductExternalShopInline(TabularDynamicInlineAdmin):

    model = ProductExternalShop


class TeamProductInline(TabularDynamicInlineAdmin):

    model = TeamProduct


class ProductKeywordInline(TabularDynamicInlineAdmin):

    model = Product.p_keywords.through


class CustomProductAdmin(ProductAdmin):

    inlines = [
        ProductExternalShopInline,
        TeamProductInline,
        ProductKeywordInline,
        ProductImageAdmin,
        ProductVariationAdmin,
        ProductLinkInline,
    ]


class ProductKeywordAdmin(BaseTranslationModelAdmin):

    model = ProductKeyword


admin.site.register(ProductList, ProductListAdmin)
admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
admin.site.register(ProductKeyword, ProductKeywordAdmin)
