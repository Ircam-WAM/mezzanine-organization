from django.contrib import admin

from django.contrib import admin
from copy import deepcopy
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from organization.core.models import *
from organization.pages.models import DynamicContentHomeSlider, DynamicContentHomeBody, Home
from organization.pages.forms import DynamicContentHomeSliderForm, DynamicContentHomeBodyForm

# Register your models here.

class DynamicContentHomeSliderInline(StackedDynamicInlineAdmin):

    model = DynamicContentHomeSlider
    form = DynamicContentHomeSliderForm


class DynamicContentHomeBodyInline(StackedDynamicInlineAdmin):

    model = DynamicContentHomeBody
    form = DynamicContentHomeBodyForm


class HomeAdminDisplayable(BaseTranslationModelAdmin):

    inlines = [DynamicContentHomeSliderInline, DynamicContentHomeBodyInline  ]


admin.site.register(Home, HomeAdminDisplayable)
