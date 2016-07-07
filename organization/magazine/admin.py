from django.contrib import admin
from django import forms
from copy import deepcopy
from mezzanine.core.admin import DisplayableAdmin
from organization.magazine.models import Brief


class BriefAdmin(admin.ModelAdmin):

    model = Brief

class BriefAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(BriefAdmin.fieldsets)

admin.site.register(Brief, BriefAdminDisplayable)
