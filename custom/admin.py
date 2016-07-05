from django.contrib import admin
from copy import deepcopy
from mezzanine.pages.models import Page
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage
from custom.models import BasicPage


# page_fieldsets = deepcopy(PageAdmin.fieldsets)
# page_fieldsets[0][1]["fields"] += ("sub_title",)
# print(page_fieldsets[0][1]["fields"])
# PageAdmin.fieldsets = page_fieldsets
#
# admin.site.unregister(RichTextPage)
# admin.site.register(RichTextPage, PageAdmin)


admin.site.register(BasicPage, PageAdmin)
