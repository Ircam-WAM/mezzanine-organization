from organization.core.admin import *
from organization.pages.admin import *
from organization.magazine.admin import *
from organization.media.admin import *
from organization.projects.admin import *
from organization.network.admin import *
from organization.agenda.admin import *
from organization.job.admin import *
from organization.shop.admin import *

from django.contrib.sessions.models import Session
from guardian.admin import GuardedModelAdmin

from organization.projects.models import *
from django.utils.translation import ugettext_lazy as _


class ProjectRepositoryInline(StackedDynamicInlineAdmin):

    model = ProjectRepository


class ProjectAdminCustomDisplayable(DisplayableAdmin, GuardedModelAdmin):

    fieldsets = (
        (None, {
            "fields": ["title", "description", "slug", "status", "is_private", "topics", "type", "owner"],
        }),
        (_("Meta data"), {
            "fields": ["_meta_title",
                       ("gen_description"),
                        "keywords", "in_sitemap"],
            "classes": ("collapse-closed",)
        }),
    )

    inlines = [ ProjectRepositoryInline,
                ProjectImageInline,
                ProjectLinkInline
                ]
    filter_horizontal = ['topics']
    list_filter = deepcopy(ProjectAdminDisplayable.list_filter)
    list_display = deepcopy(ProjectAdminDisplayable.list_display)


class ProjectTopicInline(StackedDynamicInlineAdmin):

    model = Pivot_ProjectTopic_Article


class ArticleAdminCustomDisplayable(ArticleAdminDisplayable):

    fieldsets = (
        (None, {
            "fields": ["title", "description", "slug", "status", "publish_date", "expiry_date"],
        }),
        (None, {
            "fields": ["content"],
        }),
        (_("Meta data"), {
            "fields": ["_meta_title",
                       ("gen_description"),
                        "keywords", "in_sitemap"],
            "classes": ("collapse-closed",)
        }),
    )

    inlines = [ArticleImageInline, ProjectTopicInline]


admin.site.unregister(Project)
admin.site.register(Project, ProjectAdminCustomDisplayable)
admin.site.unregister(Article)
admin.site.register(Article, ArticleAdminCustomDisplayable)
admin.site.register(Session)