from django.contrib import admin

from django.contrib import admin
from mezzanine.utils.static import static_lazy as static
from copy import deepcopy
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from organization.core.models import *
from organization.pages.models import DynamicContentHomeSlider, DynamicContentHomeBody, Home
from organization.pages.forms import DynamicContentHomeSliderForm, DynamicContentHomeBodyForm

# Register your models here.

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


admin.site.register(Home, HomeAdminDisplayable)
