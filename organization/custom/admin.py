from organization.core.admin import *
from organization.pages.admin import *
from organization.magazine.admin import *
from organization.media.admin import *
from organization.projects.admin import *
from organization.network.admin import *
from organization.agenda.admin import *
from organization.job.admin import *
from organization.shop.admin import *


class ProjectAdminCustomDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ProjectAdmin.fieldsets)
    inlines = [ ProjectBlockInline,
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
    list_filter = ['type', 'program', 'program_type', null_filter('external_id'), 'topic', 'validation_status', 'call']
    list_display = ['title', 'date_from', 'date_to', 'created', 'lead_organization',
        'program', 'status', 'is_archive', 'topic', 'external_id', 'validation_status', 'admin_link']

admin.site.unregister(Project)
admin.site.register(Project, ProjectAdminCustomDisplayable)
