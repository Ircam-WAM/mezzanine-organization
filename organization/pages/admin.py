from django.contrib import admin
from mezzanine.utils.static import static_lazy as static
from copy import deepcopy
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from organization.pages.models import *
from organization.pages.models import (
    DynamicContentHomeSlider,
    DynamicContentHomeBody,
    Home,
)
from organization.pages.forms import *
from organization.network.forms import *

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


class DynamicContentPersonListBlockInline(TabularDynamicInlineAdmin):

    model = DynamicPersonListBlockPage
    form = DynamicContentPersonListBlockForm

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


class CustomPageAdmin(PageAdmin):

    inlines = [PageBlockInline, PageImageInline, PageAudioInline, PageVideoInline, PageLinkInline, DynamicContentPersonListBlockInline]


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
# admin.site.register(PersonListBlock, PersonListBlockAdmin)
