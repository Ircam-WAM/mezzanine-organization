from copy import deepcopy
from django.contrib import admin
from organization.project.models import Project
#from custom.admin import SubTitleAdmin

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin


class ProjectAdmin(admin.ModelAdmin):

    model = Project


class ProjectAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ProjectAdmin.fieldsets)


admin.site.register(Project, ProjectAdminDisplayable)
