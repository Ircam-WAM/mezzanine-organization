from django.contrib import admin
from copy import deepcopy
from mezzanine.pages.models import Page
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage
from organization.core.models import BasicPage


admin.site.register(BasicPage, PageAdmin)
