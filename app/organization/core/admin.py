from django.contrib import admin
from copy import deepcopy
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from organization.core.models import *


class PageBlockInline(StackedDynamicInlineAdmin):

    model = PageBlock


admin.site.register(BasicPage, PageAdmin)
