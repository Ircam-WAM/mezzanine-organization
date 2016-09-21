from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.admin import *

from organization.projects.models import *
from organization.pages.models import *
from organization.media.models import Video, Audio


class ProjectLinkInline(StackedDynamicInlineAdmin):

    model = ProjectLink


class ProjectImageInline(TabularDynamicInlineAdmin):

    model = ProjectImage


class ProjectBlockInline(StackedDynamicInlineAdmin):

    model = ProjectBlock


class ProjectAudioInline(StackedDynamicInlineAdmin):

    model = ProjectAudio


class ProjectVideoInline(StackedDynamicInlineAdmin):

    model = ProjectVideo


class ProjectAdmin(admin.ModelAdmin):

    model = Project


class ProjectAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ProjectAdmin.fieldsets)
    inlines = [ ProjectBlockInline, ProjectImageInline, ProjectAudioInline, ProjectVideoInline, ProjectLinkInline]
    filter_horizontal = ['teams', 'organizations']
    list_filter = ['type', 'program', 'program_type', ]


admin.site.register(Project, ProjectAdminDisplayable)
admin.site.register(ProjectProgram)
admin.site.register(ProjectProgramType)
admin.site.register(ProjectTopic)
