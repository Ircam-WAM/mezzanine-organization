# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2019 Ircam
# Copyright (c) 2016-2019 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import csv
from django.contrib import admin
from django import forms
from django.http import HttpResponse
from copy import deepcopy
from dal import autocomplete
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user
from modeltranslation.admin import TranslationTabularInline
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from organization.network.models import *
from organization.network.forms import *
from organization.pages.forms import DynamicMultimediaPageForm
from organization.pages.models import *
from organization.core.admin import *
from organization.pages.admin import PageImageInline, PageBlockInline, PagePlaylistInline, DynamicContentPageInline, PageRelatedTitleAdmin
from organization.shop.models import PageProductList
from organization.network.utils import TimesheetXLS, set_timesheets_validation_date, flatten_activities
from organization.network.translation import *
from organization.core.utils import getUsersListOfSameTeams


class OrganizationAdminInline(StackedDynamicInlineAdmin):

    model = OrganizationLinkedInline
    form = OrganizationLinkedForm


class OrganizationLinkedAdmin(BaseTranslationOrderedModelAdmin):

    inlines = (OrganizationAdminInline,)
    first_fields = ['name',]

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


class OrganizationLinkedBlockInlineAdmin(StackedDynamicInlineAdmin):

    model = OrganizationLinkedBlockInline
    form = OrganizationLinkedListForm


class OrganizationPlaylistInline(TabularDynamicInlineAdmin):

    model = OrganizationPlaylist


class OrganizationLinkInline(StackedDynamicInlineAdmin):

    model = OrganizationLink


class OrganizationImageInline(TabularDynamicInlineAdmin):

    model = OrganizationImage


class OrganizationUserImageInline(TabularDynamicInlineAdmin):

    model = OrganizationUserImage


class OrganizationBlockInline(StackedDynamicInlineAdmin):

    model = OrganizationBlock


class OrganizationServiceInline(StackedDynamicInlineAdmin):

    model = OrganizationService


class OrganizationEventLocationInline(TranslationTabularInline):

    extra = 1
    model = OrganizationEventLocation


class ProducerDataInline(StackedDynamicInlineAdmin):

    model = ProducerData


class DynamicMultimediaOrganizationInline(TabularDynamicInlineAdmin):

    model = DynamicMultimediaOrganization
    form = DynamicMultimediaOrganizationForm


class OrganizationAdmin(BaseTranslationOrderedModelAdmin, TeamOwnableAdmin):

    model = Organization
    inlines = [ OrganizationEventLocationInline,
                OrganizationServiceInline,
                OrganizationPlaylistInline,
                DynamicMultimediaOrganizationInline,
                OrganizationImageInline,
                OrganizationBlockInline,
                OrganizationLinkInline,
                OrganizationLinkedBlockInlineAdmin,
                ProducerDataInline,
                 ]
    list_display = ['name', 'type', 'role', 'admin_thumb']
    list_filter = ['is_on_map', 'type', 'role', 'validation_status']
    search_fields = ['name',]
    first_fields = ['name',]


class OrganizationRoleAdmin(BaseTranslationModelAdmin):

    model = OrganizationRole


class PageProductListInline(TabularDynamicInlineAdmin):

    model = PageProductList


class DynamicMultimediaDepartmentInline(TabularDynamicInlineAdmin):

    model = DynamicMultimediaPage
    form = DynamicMultimediaPageForm


class DepartmentPageAdmin(PageAdmin):

    inlines = [PageImageInline, PageBlockInline, PagePlaylistInline, DynamicMultimediaDepartmentInline, PageProductListInline, ]


class DepartmentAdmin(BaseTranslationModelAdmin):

    model = Department


class TeamLinkInline(StackedDynamicInlineAdmin):

    model = TeamLink


class TeamAdmin(BaseTranslationModelAdmin, TeamOwnableAdmin):

    model = Team
    search_fields = ['name', 'code']
    list_filter = ['department']
    list_display = ['name', 'department', 'code']
    inlines = [TeamLinkInline,]


class DynamicMultimediaTeamPageInline(TabularDynamicInlineAdmin):
    
    model = DynamicMultimediaPage
    form = DynamicMultimediaPageForm


class TeamPageAdmin(PageAdmin, GuardedModelAdmin): #TeamOwnableAdmin

    inlines = [PageImageInline, PageBlockInline, PagePlaylistInline, DynamicMultimediaTeamPageInline,
                PageProductListInline, PageRelatedTitleAdmin, DynamicContentPageInline]


class PersonAdminBase(BaseTranslationModelAdmin):

    model = Person


class ActivityWeeklyHourVolumeAdmin(BaseTranslationModelAdmin):

    model = ActivityWeeklyHourVolume


class PersonActivityInline(StackedDynamicInlineAdmin):

    model = PersonActivity
    fk_name = 'person'
    filter_horizontal = ['organizations', 'employers', 'teams',
                         'supervisors', 'phd_directors', ]


class PersonPlaylistInline(TabularDynamicInlineAdmin):

    model = PersonPlaylist


class PersonLinkInline(StackedDynamicInlineAdmin):

    model = PersonLink


class PersonImageInline(TabularDynamicInlineAdmin):

    model = PersonImage


class PersonFileInline(TabularDynamicInlineAdmin):

    model = PersonFile


class PersonBlockInline(StackedDynamicInlineAdmin):

    model = PersonBlock


class DynamicMultimediaPersonInline(TabularDynamicInlineAdmin):

    model = DynamicMultimediaPerson
    form = DynamicMultimediaPersonForm


class PersonRelatedTitleAdmin(TranslationTabularInline):
    
    model = PersonRelatedTitle


class DynamicContentPersonInline(TabularDynamicInlineAdmin):

    model = DynamicContentPerson
    form = DynamicContentPersonForm


class PersonAdmin(TeamOwnableAdmin, BaseTranslationOrderedModelAdmin):

    model = Person
    inlines = [PersonImageInline,
               PersonBlockInline,
               PersonPlaylistInline,
               DynamicMultimediaPersonInline,
               PersonRelatedTitleAdmin,
               DynamicContentPersonInline,
               PersonLinkInline,
               PersonFileInline,
               PersonActivityInline,]
    first_fields = ['last_name', 'first_name', 'title', 'gender', 'user']
    search_fields = ['last_name', 'first_name']
    list_display = [ 'last_name', 'first_name', 'register_id', 'external_id', 'email', 'user', 'last_weekly_hour_volume', 'gender', 'created']
    list_filter = ['person_title', 'activities__date_from', 'activities__date_to', 'user',
                    'activities__is_permanent', 'activities__framework', 'activities__grade',
                    'activities__status', 'activities__teams',
                    'activities__weekly_hour_volume', null_filter('register_id'), null_filter('external_id')]
    actions = ['export_as_csv', ]


    def last_weekly_hour_volume(self, instance):
        last_activity = instance.activities.first()
        weekly_hour_volume = '-'
        if hasattr(last_activity, 'weekly_hour_volume'):
            if last_activity.weekly_hour_volume.__str__() != 'None':
                weekly_hour_volume = last_activity.weekly_hour_volume.__str__()
        return weekly_hour_volume

    def export_as_csv(self, request, queryset):

            meta = self.model._meta
            field_names = ['first_name', 'last_name', 'gender', 'birthday']
            activity_fields = ['date_from', 'date_to', 'framework', 'function', 'organizations', 'teams']
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
            response.write(u'\ufeff'.encode('utf8'))
            writer = csv.writer(response, delimiter=';', dialect='excel')
            activity_fields_all = []
            for i in range(10):
                activity_fields_all += activity_fields
            writer.writerow(field_names + activity_fields_all)
            for obj in queryset:
                data = [getattr(obj, field) for field in field_names]
                data += flatten_activities(obj.activities.all(), activity_fields)
                row = writer.writerow(data)

            return response

    export_as_csv.short_description = "Export Selected"


class ProjectActivityAdmin(BaseTranslationModelAdmin):

    model = ProjectActivity
    form = ProjectActivityForm
    list_display = [ 'title', 'project', 'default_percentage', 'work_package', ]
    search_fields = ['activity__person__title', 'project__title',]
    exclude = ("title", "description")

    def work_package(self, instance):
        wk_list = [str(wk.number) for wk in instance.work_packages.all()]
        return ",".join(wk_list)


class ProjectActivityInline(TabularDynamicInlineAdmin):

    model = ProjectActivity
    form = ProjectActivityForm
    exclude = ("title", "description")


class PersonActivityAdmin(BaseTranslationModelAdmin):

    model = PersonActivity
    list_display = ['person', 'get_teams', 'status', 'date_from', 'date_to']
    filter_horizontal = ['organizations', 'employers', 'teams',
                         'supervisors', 'phd_directors', ] #project_activity__project
    search_fields = ['person__title',]
    list_filter = [ 'date_from', 'date_to',
                    'is_permanent', 'framework', 'grade',
                    'status', 'teams']
    inlines = [ProjectActivityInline,]

    def get_teams(self, instance):
        values = []
        for team in instance.teams.all():
            values.append(team.code)
        return ' - '.join(values)


class PersonListBlockInlineAdmin(TabularDynamicInlineAdmin):

    model = PersonListBlockInline
    form = PersonListBlockInlineForm


class PersonListBlockAdmin(BaseTranslationModelAdmin):

    inlines = [PersonListBlockInlineAdmin,]
    search_fields = ['title', 'label',]
    list_display = ['title', 'label', 'description', 'date_created', 'date_modified']


class ActivityFunctionAdmin(BaseTranslationModelAdmin):

    model = ActivityFunction


class ActivityGradeAdmin(BaseTranslationModelAdmin):

    model = ActivityGrade


class ActivityFrameworkAdmin(BaseTranslationModelAdmin):

    model = ActivityFramework


class ActivityStatusAdmin(BaseTranslationModelAdmin):

    model = ActivityStatus


class TrainingTypeAdmin(BaseTranslationModelAdmin):

    model = TrainingType


class TrainingLevelAdmin(BaseTranslationModelAdmin):

    model = TrainingLevel


class TrainingSpecialityAdmin(BaseTranslationModelAdmin):

    model = TrainingSpeciality


class TrainingTopicAdmin(BaseTranslationModelAdmin):

    model = TrainingTopic


class PersonActivityTimeSheetAdmin(BaseTranslationOrderedModelAdmin):
    model = PersonActivityTimeSheet
    search_fields = ['year', 'month', 'activity__person__last_name', "project__title"]
    list_display = ['person', 'activity', 'year', 'month', 'project', 'work_package', 'percentage',  'accounting', 'validation']
    list_filter = ['activity__person', 'year', 'month', 'project']
    actions = ['export_xls', 'validate_timesheets']
    first_fields = ['title',]
    form = PersonActivityTimeSheetAdminForm

    def person(self, instance):
        return instance.activity.person

    def work_package(self, instance):
        wk_list = [str(wk.number) for wk in instance.work_packages.all()]
        return ",".join(wk_list)

    def export_xls(self, request, queryset):
        if request.GET.get('year') :
            xls = TimesheetXLS(queryset, request.GET.get('year'))
        else :
            xls = TimesheetXLS(queryset)
        return xls.write()

    def validate_timesheets(self, request, queryset):
        set_timesheets_validation_date(queryset)

    export_xls.short_description = "Export person timesheets"



admin.site.register(OrganizationLinked, OrganizationLinkedAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationType)
admin.site.register(OrganizationRole, OrganizationRoleAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(DepartmentPage, DepartmentPageAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamPage, TeamPageAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonListBlock, PersonListBlockAdmin)
admin.site.register(PersonActivity, PersonActivityAdmin)
admin.site.register(ActivityStatus, ActivityStatusAdmin)
admin.site.register(ActivityGrade, ActivityGradeAdmin)
admin.site.register(ActivityFramework, ActivityFrameworkAdmin)
admin.site.register(ActivityFunction, ActivityFunctionAdmin)
admin.site.register(ActivityWeeklyHourVolume, ActivityWeeklyHourVolumeAdmin)
admin.site.register(TrainingType, TrainingTypeAdmin)
admin.site.register(TrainingLevel, TrainingLevelAdmin)
admin.site.register(TrainingTopic, TrainingTopicAdmin)
admin.site.register(TrainingSpeciality, TrainingSpecialityAdmin)
admin.site.register(PersonActivityTimeSheet, PersonActivityTimeSheetAdmin)
admin.site.register(ProjectActivity, ProjectActivityAdmin)
