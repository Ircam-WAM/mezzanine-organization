from django.contrib import admin
from django import forms
from copy import deepcopy
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin

from organization.network.models import *
from organization.pages.models import *
from organization.core.admin import *


class OrganizationImageInline(TabularDynamicInlineAdmin):

    model = ModelImage


class OrganizationAdmin(BaseTranslationModelAdmin):

    model = Organization
    inlines = [OrganizationImageInline,]


class DepartmentPageBlockInline(StackedDynamicInlineAdmin):

    model = PageBlock


class DepartmentPageImageInline(TabularDynamicInlineAdmin):

    model = PageImage


class DepartmentPageAdmin(PageAdmin):

    inlines = [DepartmentPageImageInline, DepartmentPageBlockInline]


class DepartmentAdmin(BaseTranslationModelAdmin):

    model = Department


class TeamAdmin(BaseTranslationModelAdmin):

    model = Team


class TeamPageImageInline(TabularDynamicInlineAdmin):

    model = PageImage

class TeamPageBlockInline(StackedDynamicInlineAdmin):

    model = PageBlock


class TeamPageAdmin(PageAdmin):

    inlines = [TeamPageImageInline, TeamPageBlockInline]


class PersonAdminBase(BaseTranslationModelAdmin):

    model = Person


class PersonLinkInline(StackedDynamicInlineAdmin):

    model = DisplayableLink


class PersonActivityInline(StackedDynamicInlineAdmin):

    model = PersonActivity
    fk_name = 'person'


class PersonImageInline(TabularDynamicInlineAdmin):

    model = DisplayableImage


class PersonAdmin(BaseTranslationModelAdmin):

    model = Person
    inlines = [PersonImageInline, PersonActivityInline, PersonLinkInline, ]
    first_fields = ['last_name', 'first_name', 'title', 'gender', 'user']

    def get_fieldsets(self, request, obj = None):
        res = super(PersonAdmin, self).get_fieldsets(request, obj)
        for field in reversed(self.first_fields):
            index = res[0][1]['fields'].index(field)
            res[0][1]['fields'].insert(0, res[0][1]['fields'].pop(index))
        return res


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationType)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(DepartmentPage, DepartmentPageAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamPage, TeamPageAdmin)
admin.site.register(Person, PersonAdmin)
