from organization.core.admin import *
from organization.pages.admin import *
from organization.magazine.admin import *
from organization.media.admin import *
from organization.projects.admin import *
from organization.network.admin import *
from organization.agenda.admin import *
from organization.job.admin import *
from organization.shop.admin import *
from django.contrib import admin
from organization.projects.forms import *

from organization.projects.models import *
from mezzanine.generic.models import Keyword
from django.utils.translation import ugettext_lazy as _


class KeywordCustomAdmin(BaseTranslationModelAdmin):

    model = Keyword


class ProjectAdminCustomDisplayable(admin.ModelAdmin):

    model = Project
    form = ProjectAdminForm

    fieldsets = (
        (None, {
            "fields": ["title", "slug", "keywords", "status"],
        }),
        (_("Meta data"), {
            "fields": ["_meta_title",
                       ("description", "gen_description"),
                        "in_sitemap"],
            "classes": ("collapse-closed",)
        }),
    )

    inlines = [ 
                #ProjectLinkInline,
                DynamicContentProjectInline,
                ProjectImageInline,
                ]

    list_filter = deepcopy(ProjectAdminDisplayable.list_filter)
    list_display = deepcopy(ProjectAdminDisplayable.list_display)

    class Media:
        js = (
            static("mezzanine/js/admin/keyword_fields_select2.js"),
        )


admin.site.unregister(Project)
admin.site.register(Project, ProjectAdminCustomDisplayable)

admin.site.register(Keyword, KeywordCustomAdmin)
