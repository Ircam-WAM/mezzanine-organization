from django.contrib import admin
from django import forms
from copy import deepcopy
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from organization.network.models import *
from organization.network.forms import *
from organization.pages.models import *
from organization.core.admin import *
from organization.pages.admin import PageImageInline, PageBlockInline, PagePlaylistInline, DynamicContentPageInline, PageRelatedTitleAdmin
from organization.shop.models import PageProductList


class OrganizationPlaylistInline(TabularDynamicInlineAdmin):

    model = OrganizationPlaylist


class OrganizationLinkInline(StackedDynamicInlineAdmin):

    model = OrganizationLink


class OrganizationImageInline(TabularDynamicInlineAdmin):

    model = OrganizationImage


class OrganizationBlockInline(StackedDynamicInlineAdmin):

    model = OrganizationBlock


class OrganizationAdmin(BaseTranslationModelAdmin):

    model = Organization
    inlines = [ OrganizationPlaylistInline,
                OrganizationImageInline,
                OrganizationBlockInline,
                OrganizationLinkInline ]
    list_display = ['name', 'type', 'admin_thumb']
    list_filter = ['name', 'is_on_map']


class PageProductListInline(TabularDynamicInlineAdmin):

    model = PageProductList


class DepartmentPageAdmin(PageAdmin):

    inlines = [PageImageInline, PageBlockInline, PagePlaylistInline, PageProductListInline, ]


class DepartmentAdmin(BaseTranslationModelAdmin):

    model = Department


class TeamAdmin(BaseTranslationModelAdmin):

    model = Team
    search_fields = ['name', 'code']
    list_filter = ['department']
    list_display = ['name', 'department', 'code']


class TeamPageAdmin(PageAdmin):

    inlines = [PageImageInline, PageBlockInline, PagePlaylistInline,
                PageProductListInline, PageRelatedTitleAdmin, DynamicContentPageInline]


class PersonAdminBase(BaseTranslationModelAdmin):

    model = Person


class PersonActivityInline(StackedDynamicInlineAdmin):

    model = PersonActivity
    fk_name = 'person'
    filter_horizontal = ['organizations', 'employers', 'teams',
                         'projects', 'supervisors', 'phd_directors', ]


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


class PersonAdmin(BaseTranslationOrderedModelAdmin):

    model = Person
    inlines = [PersonImageInline,
               PersonBlockInline,
               PersonPlaylistInline,
               PersonLinkInline,
               PersonFileInline,
               PersonActivityInline,]
    first_fields = ['last_name', 'first_name', 'title', 'gender', 'user']
    search_fields = ['last_name', 'first_name']
    list_display = ['last_name', 'first_name', 'description', 'email', 'gender', 'created']
    list_filter = ['person_title', 'activities__date_from', 'activities__date_to',
                    'activities__is_permanent', 'activities__framework', 'activities__grade',
                    'activities__status', 'activities__teams', 'activities__projects',]


class PersonActivityAdmin(BaseTranslationModelAdmin):

    model = PersonActivity
    list_display = ['person', 'get_teams', 'status', 'date_from', 'date_to']
    filter_horizontal = ['organizations', 'employers', 'teams', 'projects',
                         'supervisors', 'phd_directors', ]

    def get_teams(self, instance):
        values = []
        for team in instance.teams.all():
            print(team.code)
            values.append(team.code)
        return ' - '.join(values)


class PersonListBlockInlineAdmin(TabularDynamicInlineAdmin):

    model = PersonListBlockInline
    form = PersonListBlockInlineForm


class PersonListBlockAdmin(admin.ModelAdmin):

    inlines = [PersonListBlockInlineAdmin,]
    list_display = ['title', 'description', 'date_created', 'date_modified']


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


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationType)
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
admin.site.register(TrainingType, TrainingTypeAdmin)
admin.site.register(TrainingLevel, TrainingLevelAdmin)
admin.site.register(TrainingTopic, TrainingTopicAdmin)
admin.site.register(TrainingSpeciality, TrainingSpecialityAdmin)
