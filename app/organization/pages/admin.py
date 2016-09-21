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
from organization.network.models import PageCustomPersonListBlockInline

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


class PersonListBlockAutocompleteInlineAdmin(TabularDynamicInlineAdmin):

    model = PageCustomPersonListBlockInline
    form = PageCustomPersonListForm


class CustomPageAdmin(PageAdmin):

    inlines = [PageBlockInline,
            PageImageInline,
            PageAudioInline,
            PageVideoInline,
            PageLinkInline,
            PersonListBlockAutocompleteInlineAdmin,
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
