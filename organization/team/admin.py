from django.contrib import admin
from django import forms
from copy import deepcopy
from mezzanine.core.admin import *
from organization.team.models import *


class OrganizationAdmin(BaseTranslationModelAdmin):

    model = Organization


class DepartmentAdmin(BaseTranslationModelAdmin):

    model = Department


class TeamAdmin(BaseTranslationModelAdmin):

    model = Team


class ActivityAdmin(BaseTranslationModelAdmin):

    model = Activity


class ActivityInline(StackedDynamicInlineAdmin):

    model = Activity


class PersonAdminBase(admin.ModelAdmin):

    model = Person

#
# class PersonAdmin(BaseTranslationModelAdmin):
#
#     model = Person
#     inlines = [ActivityInline,]
#
#     def get_fieldsets(self, request, obj = None):
#         res = super(PersonAdmin, self).get_fieldsets(request, obj)
#         # I only need to move one field; change the following
#         # line to account for more.
#         fields = (res[0][1]['fields'])
#
#         res[0][1]['fields'].append(res[0][1]['fields'].pop(0))
#         return res

class PersonAdmin(BaseTranslationModelAdmin):

    model = Person
    inlines = [ActivityInline,]
    first_fields = ['first_name', 'last_name', 'title', 'gender', 'user']

    def get_fieldsets(self, request, obj = None):
        res = super(PersonAdmin, self).get_fieldsets(request, obj)
        for field in reversed(self.first_fields):
            index = res[0][1]['fields'].index(field)
            res[0][1]['fields'].insert(0, res[0][1]['fields'].pop(index))
        return res



admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationType)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Activity, ActivityAdmin)
