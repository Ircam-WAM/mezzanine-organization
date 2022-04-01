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
from mezzanine.pages.models import Page, RichText
from modeltranslation.translator import TranslationOptions
from mezzanine.core.translation import (TranslatedSlugged,
                                        TranslatedDisplayable,
                                        TranslatedRichText)
from organization.magazine.models import *


@register(Article)
class ArticleTranslationOptions(TranslationOptions):

    fields = ('sub_title',)


@register(Brief)
class BriefTranslationOptions(TranslationOptions):

    fields = ('title', 'content', 'text_button', )


@register(Topic)
class TopicTranslationOptions(TranslationOptions):

    fields = ('content',)


@register(ArticleImage)
class ArticleImageTranslationOptions(TranslationOptions):

    fields = ('description',)


@register(ArticlePersonListBlockInline)
class ArticlePersonListBlockInlineTranslationOptions(TranslationOptions):

    pass


@register(DynamicContentArticle)
class DynamicContentArticleTranslationOptions(TranslationOptions):

    pass


@register(DynamicMultimediaArticle)
class DynamicMultimediaArticleTranslationOptions(TranslationOptions):

    fields = ()


@register(ArticlePlaylist)
class ArticlePlaylistTranslationOptions(TranslationOptions):

    pass


@register(ArticleRelatedTitle)
class ArticleRelatedTitleTranslationOptions(TranslationOptions):

    fields = ('title', )


@register(Magazine)
class MagazineTranslationOptions(TranslationOptions):

    fields = ('title', 'description', )


@register(DynamicContentMagazineContent)
class DynamicContentMagazineContentTranslationOptions(TranslationOptions):

    pass


@register(GalleryImage)
class DynamicContentMagazineContentTranslationOptions(TranslationOptions):

    pass