from django.contrib import admin
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


class PageAudioInline(StackedDynamicInlineAdmin):

    model = PageAudio
    exclude = ("short_url", "keywords", "description", "slug", )


class PageVideoInline(StackedDynamicInlineAdmin):

    model = PageVideo
    exclude = ("short_url", "keywords", "description", "slug", )


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


class CustomPageAdmin(PageAdmin):

    inlines = [PageBlockInline,
            PageImageInline,
            PageAudioInline,
            PageVideoInline,
            PageLinkInline,
            PersonListBlockAutocompleteInlineAdmin,
            PageProductListInline,
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


class HomeAdminDisplayable(BaseTranslationModelAdmin):

    inlines = [DynamicContentHomeSliderInline, DynamicContentHomeBodyInline  ]


admin.site.register(CustomPage, CustomPageAdmin)
admin.site.register(Home, HomeAdminDisplayable)
admin.site.unregister(MezzanineLink)
admin.site.register(MezzanineLink, LinkImageAdmin)
