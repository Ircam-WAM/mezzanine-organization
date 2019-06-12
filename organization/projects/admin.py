# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
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

from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from pprint import pprint
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from modeltranslation.admin import TranslationTabularInline
from organization.projects.models import *
from organization.pages.models import *
from organization.media.models import Playlist
from organization.pages.admin import PageImageInline
from organization.projects.forms import DynamicContentProjectForm, DynamicMultimediaProjectForm, DynamicContentProjectPageForm
from organization.core.admin import null_filter, BaseTranslationOrderedModelAdmin, TeamOwnableAdmin
from organization.core.utils import actions_to_duplicate, get_other_sites


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


class ProjectDemoInline(TabularDynamicInlineAdmin):

    model = ProjectDemo


class ProjectPageInline(StackedDynamicInlineAdmin):

    model = ProjectPage


class ProjectWorkPackageInline(TabularDynamicInlineAdmin):

    model = ProjectWorkPackage


class ProjectDemoAdmin(BaseTranslationModelAdmin):

    model = ProjectDemo
    filter_horizontal = ['authors']


class ProjectBlogPageInline(StackedDynamicInlineAdmin):

    model = ProjectBlogPage


class ProjectUserImageInline(StackedDynamicInlineAdmin):

    model = ProjectUserImage


class ProjectContactInline(StackedDynamicInlineAdmin):

    model = ProjectContact


class ProjectPublicDataAdmin(admin.ModelAdmin):

    model = ProjectPublicData
    list_display = ['project',]


class ProjectPrivateDataAdmin(admin.ModelAdmin):

    model = ProjectPrivateData
    list_display = ['project',]


class ProjectContactAdmin(admin.ModelAdmin):

    model = ProjectContact
    list_display = ['project',]


class ProjectPublicDataInline(StackedDynamicInlineAdmin):

    model = ProjectPublicData


class ProjectPrivateDataInline(StackedDynamicInlineAdmin):

    model = ProjectPrivateData


class ProjectRelatedTitleAdmin(TranslationTabularInline):

    model = ProjectRelatedTitle


class DynamicContentProjectInline(TabularDynamicInlineAdmin):

    model = DynamicContentProject
    form = DynamicContentProjectForm

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


class DynamicMultimediaProjectInline(TabularDynamicInlineAdmin):

    model = DynamicMultimediaProject
    form = DynamicMultimediaProjectForm


class ProjectResidencyProducerInline(TabularDynamicInlineAdmin):

    model = ProjectResidencyProducer


class ProjectResidencyImageInline(StackedDynamicInlineAdmin):

    model = ProjectResidencyImage


class ProjectResidencyUserImageInline(StackedDynamicInlineAdmin):

    model = ProjectResidencyUserImage


class ProjectResidencyArticleInline(TabularDynamicInlineAdmin):

    model = ProjectResidencyArticle


class ProjectResidencyEventInline(TabularDynamicInlineAdmin):

    model = ProjectResidencyEvent


class ProjectResidencyAdmin(admin.ModelAdmin):

    model = ProjectResidency
    list_display = ["title", "project", "artist", "get_producers", "validated",]
    list_filter = ["validated"]
    inlines = [ ProjectResidencyProducerInline,
                ProjectResidencyImageInline,
                ProjectResidencyUserImageInline,
                ProjectResidencyArticleInline,
                ProjectResidencyEventInline,
                ]

    def get_producers(self, obj):
        producers = ""
        if obj.producers:
            names = []
            for producer in obj.producers.all():
                names.append(producer.organization.name)
            producers = ", ".join(names)
        return producers

    get_producers.short_description = "producers"


class ProjectAdmin(BaseTranslationOrderedModelAdmin):

    model = Project

    inlines = [ ProjectBlockInline,
                ProjectContactInline,
                ProjectUserImageInline,
                ProjectImageInline,
                ProjectPublicDataInline,
                ProjectPrivateDataInline,
                ProjectWorkPackageInline,
                ProjectPageInline,
                ProjectPlaylistInline,
                DynamicMultimediaProjectInline,
                ProjectLinkInline,
                ProjectFileInline,
                ProjectRelatedTitleAdmin,
                DynamicContentProjectInline,
                ProjectBlogPageInline,
                ]
    filter_horizontal = ['teams', 'organizations', 'concepts']
    search_fields = ['title', ]
    list_filter = ['type', 'program', 'program_type', null_filter('external_id'), 'topic', 'validation_status', 'call']
    list_display = ['title', 'date_from', 'date_to', 'created', 'lead_organization',
        'program', 'is_archive', 'topic', 'external_id', 'validation_status']
    first_fields = ['title',]


class ProjectTopicAdmin(BaseTranslationModelAdmin):

    model = ProjectTopic


class ProjectProgramAdmin(BaseTranslationModelAdmin):

    model = ProjectProgram


class ProjectProgramTypeAdmin(BaseTranslationModelAdmin):

    model = ProjectProgramType


class ProjectTopicPageAdmin(PageAdmin):

    inlines = [PageImageInline, ]


class ProjectWorkPackageAdmin(BaseTranslationModelAdmin):

    model = ProjectWorkPackage
    list_display = ['title', 'project', 'date_from', 'date_to', 'number', 'lead_organization' ]
    list_filter = ['project', 'date_from', 'date_to', 'lead_organization' ]

class ProjectCallAdmin(admin.ModelAdmin):

    model = ProjectCall


class ProjectCallBlockInline(StackedDynamicInlineAdmin):

    model = ProjectCallBlock


class ProjectCallLinkInline(StackedDynamicInlineAdmin):

    model = ProjectCallLink


class ProjectCallImageInline(StackedDynamicInlineAdmin):

    model = ProjectCallImage


class ProjectCallFileInline(StackedDynamicInlineAdmin):

    model = ProjectCallFile


class ProjectCallAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ProjectCallAdmin.fieldsets)
    inlines = [ ProjectCallBlockInline,
                ProjectCallImageInline,
                ProjectCallLinkInline,
                ProjectCallFileInline,
                ]
    # list_filter = ['type', 'program', 'program_type', null_filter('external_id')]
    # list_display = ['title', 'date_from', 'date_to', 'status', 'admin_link']

    search_fields = ['title', 'project__title',]



class ProjectPageAdmin(BaseTranslationModelAdmin):

    model = ProjectPage
    list_display = ['title', 'project', ]
    list_filter = ['project', ]


class ProjectPageBlockInline(StackedDynamicInlineAdmin):

    model = ProjectPageBlock


class ProjectPageImageInline(StackedDynamicInlineAdmin):

    model = ProjectPageImage


class DynamicContentProjectPageInline(TabularDynamicInlineAdmin):

    model = DynamicContentProjectPage
    form = DynamicContentProjectPageForm

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )

class ProjectPageAdminDisplayable(DisplayableAdmin): #, DuplicateAdmin

    fieldsets = deepcopy(ProjectPageAdmin.fieldsets)
    inlines = [ ProjectPageBlockInline,
                ProjectPageImageInline,
                DynamicContentProjectPageInline,
                ]
    # list_filter = ['type', 'program', 'program_type', null_filter('external_id')]
    # list_display = ['title', 'date_from', 'date_to', 'status', 'admin_link']
    actions = actions_to_duplicate()
    search_fields = ['title', 'project__title',]



admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectPublicData, ProjectPublicDataAdmin)
admin.site.register(ProjectPrivateData, ProjectPrivateDataAdmin)
admin.site.register(ProjectContact, ProjectContactAdmin)
admin.site.register(ProjectProgram, ProjectProgramAdmin)
admin.site.register(ProjectProgramType, ProjectProgramTypeAdmin)
admin.site.register(ProjectTopic, ProjectTopicAdmin)
admin.site.register(ProjectTopicPage, ProjectTopicPageAdmin)
admin.site.register(ProjectDemo, ProjectDemoAdmin)
admin.site.register(Repository)
admin.site.register(RepositorySystem)
admin.site.register(ProjectWorkPackage, ProjectWorkPackageAdmin)
admin.site.register(ProjectCall, ProjectCallAdminDisplayable)
admin.site.register(ProjectResidency, ProjectResidencyAdmin)
admin.site.register(ProjectPage, ProjectPageAdminDisplayable)