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
from modeltranslation.admin import TranslationTabularInline
from mezzanine.utils.static import static_lazy as static
from mezzanine.core.admin import StackedDynamicInlineAdmin, BaseTranslationModelAdmin,\
    TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin, LinkAdmin
from mezzanine.pages.models import Link as MezzanineLink
from organization.pages.models import PageBlock, PageImage, PageAction, \
    PagePlaylist, PageLink, LinkImage, LinkStyle, DynamicContentPage,\
    PageRelatedTitle, DynamicMultimediaPage, ExtendedCustomPageDynamicContent,\
    DynamicContentHomeMedia, HomeImage, CustomPage, ExtendedCustomPage
from organization.pages.models import (
    DynamicContentHomeSlider,
    DynamicContentHomeBody,
    Home,
)

from organization.pages.forms import DynamicContentPageForm, DynamicMultimediaPageForm,\
    DynamicContentHomeSliderForm, DynamicContentHomeBodyForm,\
    DynamicContentHomeMediaForm
from organization.network.forms import PageCustomPersonListForm
from organization.network.models import PageCustomPersonListBlockInline
from organization.shop.models import PageProductList


class PageBlockInline(StackedDynamicInlineAdmin):

    model = PageBlock
    model_name = "PageBlock"
    template = 'admin/pages/custompage/edit_inline/stacked.html'


class PageImageInline(TabularDynamicInlineAdmin):

    model = PageImage
    model_name = "PageImage"
    template = 'admin/pages/custompage/edit_inline/tabular.html'


class PagePlaylistInline(TabularDynamicInlineAdmin):

    model = PagePlaylist
    model_name = "PagePlaylist"
    template = 'admin/pages/custompage/edit_inline/tabular.html'


class PageLinkInline(StackedDynamicInlineAdmin):

    model = PageLink
    model_name = "PageLink"


class LinkImageInline(StackedDynamicInlineAdmin):

    model = LinkImage


class PageActionInline(StackedDynamicInlineAdmin):

    model = PageAction


class LinkStyleInline(TabularDynamicInlineAdmin):

    model = LinkStyle
    template = 'admin/pages/custompage/edit_inline/stacked.html'


class LinkImageAdmin(LinkAdmin):

    inlines = [LinkStyleInline, LinkImageInline]


class PersonListBlockAutocompleteInlineAdmin(TabularDynamicInlineAdmin):

    model = PageCustomPersonListBlockInline
    model_name = "PageCustomPersonListBlockInline"
    exclude = ("title", "description")
    form = PageCustomPersonListForm
    template = 'admin/pages/custompage/edit_inline/tabular.html'


class PageProductListInline(TabularDynamicInlineAdmin):

    model = PageProductList
    model_name = "PageProductList"
    template = 'admin/pages/custompage/edit_inline/tabular.html'


class DynamicContentPageInline(TabularDynamicInlineAdmin):

    model = DynamicContentPage
    model_name = "DynamicContentPage"
    form = DynamicContentPageForm
    template = 'admin/pages/custompage/edit_inline/tabular.html'

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


class PageRelatedTitleAdmin(TranslationTabularInline):

    model = PageRelatedTitle
    model_name = "PageRelatedTitle"
    template = 'admin/pages/custompage/edit_inline/tabular.html'


class DynamicMultimediaPageInline(TabularDynamicInlineAdmin):

    model = DynamicMultimediaPage
    model_name = "DynamicMultimediaPage"
    form = DynamicMultimediaPageForm
    template = 'admin/pages/custompage/edit_inline/tabular.html'


class CustomPageAdmin(PageAdmin):

    inlines = [
        PageLinkInline,
        PageImageInline,
        PagePlaylistInline,
        DynamicMultimediaPageInline,
        PageBlockInline,
        PersonListBlockAutocompleteInlineAdmin,
        PageProductListInline,
        PageRelatedTitleAdmin,
        DynamicContentPageInline,
        PageActionInline,
    ]

    change_form_template = "admin/pages/custompage/change_form.html"


class ExtendedCustomPageDynamicContentInline(TabularDynamicInlineAdmin):

    model = ExtendedCustomPageDynamicContent


class ExtendedCustomPageAdmin(PageAdmin):

    inlines = [
        PageBlockInline,
        PageImageInline,
        PagePlaylistInline,
        PageLinkInline,
        PageProductListInline,
        PageRelatedTitleAdmin,
        ExtendedCustomPageDynamicContentInline,
        DynamicContentPageInline
    ]


class DynamicContentHomeSliderInline(TabularDynamicInlineAdmin):

    model = DynamicContentHomeSlider
    form = DynamicContentHomeSliderForm

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


class DynamicContentHomeBodyInline(TabularDynamicInlineAdmin):

    model = DynamicContentHomeBody
    form = DynamicContentHomeBodyForm


class DynamicContentHomeMediaInline(TabularDynamicInlineAdmin):

    model = DynamicContentHomeMedia
    form = DynamicContentHomeMediaForm


class HomeImageInline(TabularDynamicInlineAdmin):

    model = HomeImage


class HomeAdminDisplayable(BaseTranslationModelAdmin):

    inlines = [
        HomeImageInline,
        DynamicContentHomeSliderInline,
        DynamicContentHomeMediaInline,
        DynamicContentHomeBodyInline,
    ]


admin.site.register(CustomPage, CustomPageAdmin)
admin.site.register(ExtendedCustomPage, ExtendedCustomPageAdmin)
admin.site.register(Home, HomeAdminDisplayable)
admin.site.unregister(MezzanineLink)
admin.site.register(MezzanineLink, LinkImageAdmin)
