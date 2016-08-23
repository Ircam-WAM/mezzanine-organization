from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.admin import *

from organization.projects.models import *
from organization.pages.models import *


class ProjectLinkInline(StackedDynamicInlineAdmin):

    model = DisplayableLink


class ProjectImageInline(TabularDynamicInlineAdmin):

    model = DisplayableImage


class ProjectBlockInline(StackedDynamicInlineAdmin):

    model = DisplayableBlock


class ProjectAdmin(admin.ModelAdmin):

    model = Project


class ProjectAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ProjectAdmin.fieldsets)
    inlines = [ProjectImageInline, ProjectBlockInline, ProjectLinkInline, ]
    filter_horizontal = ['persons', 'teams', 'organizations']


admin.site.register(Project, ProjectAdminDisplayable)
