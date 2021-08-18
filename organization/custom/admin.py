from copy import deepcopy

from django.contrib import admin

from organization.core.admin import DisplayableAdmin, null_filter
from organization.projects.admin import ProjectAdmin, ProjectBlockInline,\
    ProjectContactInline, ProjectUserImageInline, ProjectImageInline,\
    ProjectPublicDataInline, ProjectPrivateDataInline, ProjectWorkPackageInline,\
    ProjectPlaylistInline, ProjectLinkInline, ProjectFileInline,\
    ProjectRelatedTitleAdmin, DynamicContentProjectInline, ProjectBlogPageInline
from organization.projects.models import Project


class ProjectAdminCustomDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ProjectAdmin.fieldsets)
    inlines = [
        ProjectBlockInline,
        ProjectContactInline,
        ProjectUserImageInline,
        ProjectImageInline,
        ProjectPublicDataInline,
        ProjectPrivateDataInline,
        ProjectWorkPackageInline,
        ProjectPlaylistInline,
        ProjectLinkInline,
        ProjectFileInline,
        ProjectRelatedTitleAdmin,
        DynamicContentProjectInline,
        ProjectBlogPageInline,
    ]
    filter_horizontal = ['teams', 'organizations']
    list_filter = [
        'type',
        'program',
        'program_type',
        null_filter('external_id'),
        'topic',
        'validation_status',
        'call'
    ]
    list_display = [
        'title',
        'date_from',
        'date_to',
        'created',
        'lead_organization',
        'program',
        'status',
        'is_archive',
        'topic',
        'external_id',
        'validation_status',
        'admin_link'
    ]


admin.site.unregister(Project)
admin.site.register(Project, ProjectAdminCustomDisplayable)
