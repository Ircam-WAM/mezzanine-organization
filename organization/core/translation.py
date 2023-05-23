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

from modeltranslation.translator import register, TranslationOptions
from mezzanine.generic.models import Keyword
from .models import Image, MetaCategory


@register(Keyword)
class KeywordTranslationOptions(TranslationOptions):

    fields = ('title',)


@register(Image)
class ImageTranslationOptions(TranslationOptions):

    fields = ('title', 'credits')


@register(MetaCategory)
class MetaCategoryTranslationOptions(TranslationOptions):

    fields = ('name', 'description')
