from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin

from organization.projects.models import *
from organization.pages.models import *
from organization.media.models import Playlist
from organization.pages.admin import PageImageInline


class ProjectLinkInline(StackedDynamicInlineAdmin):

    model = ProjectLink


class ProjectImageInline(TabularDynamicInlineAdmin):

    model = ProjectImage


class ProjectBlockInline(StackedDynamicInlineAdmin):

    model = ProjectBlock


class ProjectPlaylistInline(TabularDynamicInlineAdmin):

    model = ProjectPlaylist


class ProjectFileInline(TabularDynamicInlineAdmin):

    model = ProjectFile


class ProjectAdmin(admin.ModelAdmin):

    model = Project


class ProjectAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ProjectAdmin.fieldsets)
    inlines = [ ProjectBlockInline,
                ProjectImageInline,
                ProjectPlaylistInline,
                ProjectLinkInline,
                ProjectFileInline]
    filter_horizontal = ['teams', 'organizations']
    list_filter = ['type', 'program', 'program_type', ]


class ProjectTopicAdmin(BaseTranslationModelAdmin):

    model = ProjectTopic


class ProjectProgramAdmin(BaseTranslationModelAdmin):

    model = ProjectProgram


class ProjectProgramTypeAdmin(BaseTranslationModelAdmin):

    model = ProjectProgramType


class ProjectTopicPageAdmin(PageAdmin):

    inlines = [PageImageInline, ]



admin.site.register(Project, ProjectAdminDisplayable)
admin.site.register(ProjectProgram, ProjectProgramAdmin)
admin.site.register(ProjectProgramType, ProjectProgramTypeAdmin)
admin.site.register(ProjectTopic, ProjectTopicAdmin)
admin.site.register(ProjectTopicPage, ProjectTopicPageAdmin)
