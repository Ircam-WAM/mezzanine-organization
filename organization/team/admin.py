from django.contrib import admin
from django import forms
from copy import deepcopy
from mezzanine.core.admin import DisplayableAdmin, BaseDynamicInlineAdmin, BaseTranslationModelAdmin
from organization.team.models import *



class ActivityInline(admin.StackedInline):

    model = Activity
    extras = 3


class PersonAdmin(admin.ModelAdmin):

    model = Person


class PersonAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(PersonAdmin.fieldsets)
    inlines = [ActivityInline,]


admin.site.register(Organization)
admin.site.register(OrganizationType)
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Person, PersonAdminDisplayable)
admin.site.register(Activity)
