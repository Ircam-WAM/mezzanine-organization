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
from organization.pages.admin import PageImageInline, PageBlockInline, PageAudioInline, PageVideoInline


class OrganizationAudioInline(StackedDynamicInlineAdmin):

    model = OrganizationAudio


class OrganizationVideoInline(StackedDynamicInlineAdmin):

    model = OrganizationVideo


class OrganizationLinkInline(StackedDynamicInlineAdmin):

    model = OrganizationLink


class OrganizationImageInline(TabularDynamicInlineAdmin):

    model = OrganizationImage


class OrganizationBlockInline(StackedDynamicInlineAdmin):

    model = OrganizationBlock


class OrganizationAdmin(BaseTranslationModelAdmin):

    model = Organization
    inlines = [ OrganizationAudioInline,
                OrganizationImageInline,
                OrganizationVideoInline,
                OrganizationBlockInline,
                OrganizationLinkInline ]


class DepartmentPageAdmin(PageAdmin):

    inlines = [PageImageInline, PageBlockInline, PageAudioInline, PageVideoInline, ]


class DepartmentAdmin(BaseTranslationModelAdmin):

    model = Department


class TeamAdmin(BaseTranslationModelAdmin):

    model = Team


class TeamPageAdmin(PageAdmin):

    inlines = [PageImageInline, PageBlockInline, PageAudioInline, PageVideoInline, ]


class PersonAdminBase(BaseTranslationModelAdmin):

    model = Person


class PersonActivityInline(StackedDynamicInlineAdmin):

    model = PersonActivity
    fk_name = 'person'


class PersonAudioInline(StackedDynamicInlineAdmin):

    model = PersonAudio


class PersonVideoInline(StackedDynamicInlineAdmin):

    model = PersonVideo


class PersonLinkInline(StackedDynamicInlineAdmin):

    model = PersonLink


class PersonImageInline(TabularDynamicInlineAdmin):

    model = PersonImage


class PersonBlockInline(StackedDynamicInlineAdmin):

    model = PersonBlock


class PersonAdmin(BaseTranslationOrderedModelAdmin):

    model = Person
    inlines = [PersonActivityInline, PersonAudioInline, PersonImageInline, PersonVideoInline, PersonBlockInline, PersonLinkInline ]
    first_fields = ['last_name', 'first_name', 'title', 'gender', 'user']
    search_fields = ['last_name', 'first_name']


class PersonListBlockInlineAdmin(TabularDynamicInlineAdmin):

    model = PersonListBlockInline
    form = PersonListBlockInlineForm


class PersonListBlockAdmin(admin.ModelAdmin):

    inlines = [PersonListBlockInlineAdmin,]


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationType)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(DepartmentPage, DepartmentPageAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamPage, TeamPageAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonListBlock, PersonListBlockAdmin)
admin.site.register(ActivityStatus)
admin.site.register(ActivityGrade)
admin.site.register(ActivityFramework)
admin.site.register(ActivityFunction)
admin.site.register(TrainingType)
admin.site.register(TrainingLevel)
admin.site.register(TrainingTopic)
admin.site.register(TrainingSpeciality)
