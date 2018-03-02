from organization.core.admin import *
from organization.pages.admin import *
from organization.magazine.admin import *
from organization.media.admin import *
from organization.projects.admin import *
from organization.network.admin import *
from organization.agenda.admin import *
from organization.job.admin import *
from organization.shop.admin import *

from organization.projects.models import Project


class ProjectAdminCustomDisplayable(DisplayableAdmin):

    inlines = [ DynamicContentProjectInline,
                ProjectImageInline,
                ProjectLinkInline,
                ]
    filter_horizontal = deepcopy(ProjectAdminDisplayable.filter_horizontal)
    list_filter = deepcopy(ProjectAdminDisplayable.list_filter)
    list_display = deepcopy(ProjectAdminDisplayable.list_display)

admin.site.unregister(Project)
admin.site.register(Project, ProjectAdminCustomDisplayable)
