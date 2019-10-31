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

from modeltranslation.translator import translator, register, TranslationOptions

from organization.shop.models import *



@register(ProductList)
class ProductListTranslationOptions(TranslationOptions):

    fields = ['title', 'description', 'content']


@register(ProductListProduct)
class ProductListProductTranslationOptions(TranslationOptions):

    pass


@register(PageProductList)
class PageProductListTranslationOptions(TranslationOptions):

    pass


@register(ProductLink)
class ProductLinkTranslationOptions(TranslationOptions):

    fields = ('title',)


@register(ProductExternalShop)
class ProductExternalShopTranslationOptions(TranslationOptions):

    pass


@register(TeamProduct)
class TeamProductTranslationOptions(TranslationOptions):

    pass


@register(CustomProductImage)
class CustomProductImageranslationOptions(TranslationOptions):

    pass