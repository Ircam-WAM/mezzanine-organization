from django.contrib import admin
from modeltranslation.admin import TranslationTabularInline
from mezzanine.utils.static import static_lazy as static
from copy import deepcopy
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin, LinkAdmin
from mezzanine.pages.models import Link as MezzanineLink
from organization.pages.models import *
from organization.pages.models import (
    DynamicContentHomeSlider,
    DynamicContentHomeBody,
    Home,
)
from organization.pages.forms import *
from organization.network.forms import *
from organization.network.models import PageCustomPersonListBlockInline
from organization.shop.models import *


class PageBlockInline(StackedDynamicInlineAdmin):

    model = PageBlock


class PageImageInline(TabularDynamicInlineAdmin):

    model = PageImage


class PagePlaylistInline(TabularDynamicInlineAdmin):

    model = PagePlaylist


class PageLinkInline(StackedDynamicInlineAdmin):

    model = PageLink


class LinkImageInline(StackedDynamicInlineAdmin):

    model = LinkImage


class LinkImageAdmin(LinkAdmin):

    inlines = [LinkImageInline,]


class PersonListBlockAutocompleteInlineAdmin(TabularDynamicInlineAdmin):

    model = PageCustomPersonListBlockInline
    form = PageCustomPersonListForm


class PageProductListInline(TabularDynamicInlineAdmin):

    model = PageProductList


class DynamicContentPageInline(TabularDynamicInlineAdmin):

    model = DynamicContentPage
    form = DynamicContentPageForm

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


class PageRelatedTitleAdmin(TranslationTabularInline):

    model = PageRelatedTitle


class CustomPageAdmin(PageAdmin):

    inlines = [PageBlockInline,
            PageImageInline,
            PagePlaylistInline,
            PageLinkInline,
            PersonListBlockAutocompleteInlineAdmin,
            PageProductListInline,
            PageRelatedTitleAdmin,
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


class HomeAdminDisplayable(BaseTranslationModelAdmin):

    inlines = [ DynamicContentHomeSliderInline,
                DynamicContentHomeMediaInline,
                DynamicContentHomeBodyInline,
                ]


admin.site.register(CustomPage, CustomPageAdmin)
admin.site.register(Home, HomeAdminDisplayable)
admin.site.unregister(MezzanineLink)
admin.site.register(MezzanineLink, LinkImageAdmin)
