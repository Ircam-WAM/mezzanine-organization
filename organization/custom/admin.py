from organization.core.admin import *
from organization.pages.admin import *
from organization.magazine.admin import *
from organization.media.admin import *
from organization.projects.admin import *
from organization.network.admin import *
from organization.agenda.admin import *
from organization.job.admin import *
from organization.shop.admin import *

from organization.projects.models import *
from django.utils.translation import ugettext_lazy as _


class ProjectAdminCustomDisplayable(DisplayableAdmin):

    fieldsets = (
        (None, {
            "fields": ["title", "description", "slug", "status", "topics"],
        }),
        (_("Meta data"), {
            "fields": ["_meta_title",
                       ("gen_description"),
                        "keywords", "in_sitemap"],
            "classes": ("collapse-closed",)
        }),
    )

    inlines = [ ProjectLinkInline,
                ProjectImageInline,
                ]
    filter_horizontal = ['topics']
    list_filter = deepcopy(ProjectAdminDisplayable.list_filter)
    list_display = deepcopy(ProjectAdminDisplayable.list_display)


admin.site.unregister(Project)
admin.site.register(Project, ProjectAdminCustomDisplayable)
