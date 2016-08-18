from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.admin import *

from organization.project.models import *


class ProjectLinkInline(StackedDynamicInlineAdmin):

    model = ProjectLink


class ProjectImageInline(TabularDynamicInlineAdmin):

    model = ProjectImage


class ProjectBlockInline(StackedDynamicInlineAdmin):

    model = ProjectBlock


class ProjectAdmin(admin.ModelAdmin):

    model = Project


class ProjectAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ProjectAdmin.fieldsets)
    inlines = [ProjectImageInline, ProjectBlockInline, ProjectLinkInline, ]


admin.site.register(Project, ProjectAdminDisplayable)
