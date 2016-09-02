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
    filter_horizontal = ['persons', 'teams', 'organizations']


admin.site.register(Project, ProjectAdminDisplayable)