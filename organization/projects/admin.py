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
from organization.projects.forms import DynamicContentProjectForm
from organization.core.admin import null_filter
from organization.projects.translation import *
from organization.projects.forms import DynamicContentProjectForm, DynamicMultimediaProjectForm, DynamicContentProjectPageForm
from organization.core.admin import null_filter, BaseTranslationOrderedModelAdmin #, DuplicateAdmin
from organization.core.utils import actions_to_duplicate, get_other_sites
from organization.network.admin import TeamOwnableAdmin
import csv
from django.http import HttpResponse
from django.core.files.base import ContentFile
import os.path
from django.conf import settings


def export_projects_as_csv(modeladmin, request, queryset):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vertigo_projects.csv"'
    writer = csv.writer(response, delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)
    writer.writerow([
        "Project name",
        "ID",
        "User",
        "Slug",
        "Call",
        "Call slug",
        "Created",
        "Validation status",
        "Topic",
        "Organization name",
        "Website",
        "Dimension",
        "Funding type",
        "Funding programme",
        "Date from",
        "Date to",
        "Persons",
        "First name",
        "Last name",
        "Telephone",
        "Email",
        "Position",
        "Postal code",
        "City",
        "Country",
        "Address",
        "Brief description",
        "Technology description",
        "Keywords",
        "Project description",
        "Resources description",
        "Challenges description",
        "Objectives description",
        "Residency start date",
        "Perior for direct cooperation",
        "Residency duration"
    ])
    # Retrieve the Projects
    for obj in queryset:
        call = obj.call.name if obj.call else ""
        call_slug = obj.call.slug if obj.call else ""
        created = obj.created.strftime("%Y-%m-%d %H:%M:%S") if obj.created else ""
        validation_status = str(dict(PROJECT_VALIDATION_STATUS_CHOICES).get(obj.validation_status)) if obj.validation_status else ""
        topic = obj.topic.name if obj.topic else ""
        public_data = obj.public_data.all().first() if obj.public_data.all().first() else ProjectPublicData()
        private_data = obj.private_data.all().first() if obj.private_data.all().first() else ProjectPrivateData()
        contact = obj.contacts.all().first() if obj.contacts.all().first() else ProjectContact()
        country = str(contact.country.name) if contact.country else ""
        writer.writerow([
            obj.title, # Project name
            obj.id, # ID
            obj.user, # User
            obj.slug, # Slug
            call, # Call
            call_slug, # Call slug
            created, # Created
            validation_status, # Validation status
            topic, # Topic
            contact.organization_name, # Organization name
            obj.website, # Website
            private_data.dimension, # Dimension
            obj.funding, # Funding
            private_data.funding_programme, # Funding programme
            obj.date_from, # Date from
            obj.date_to, # Date to
            private_data.persons, # Persons
            contact.first_name, # First name
            contact.last_name, # Last name
            contact.telephone, # Telephone
            contact.email, # Email
            contact.position, # Position
            contact.postal_code, # Postal code
            contact.city, # City
            country, # Country
            contact.address, # Address
            public_data.brief_description, # Brief description
            public_data.technology_description, # Technology description
            obj.keywords, # Keywords
            private_data.description, # Project description
            public_data.resources_description, # Resources description
            public_data.challenges_description, # Challenges description
            public_data.objectives_description, # Objectives description
            public_data.implementation_start_date, # Residency start date
            public_data.implementation_period, # Perior for direct cooperation
            public_data.implementation_duration # Residency duration
        ])
    # Return the CSV file
    return response


export_projects_as_csv.short_description = "Export selected Projects as CSV"


def add_name_numbering(name):
    # Append {f_name}-{f_number}.{f_extension} to the name. Examples:
    # "A.jpg"   -> "A-1.jpg"
    # "A-1.jpg" -> "A-2.jpg"
    # "A"       -> "A-1"
    # ""        -> None
    if not isinstance(name, str) or not name:
        return None
    f_name = ""
    f_number = ""
    f_ext = ""
    # Get extension
    name_list = name.split(".")
    if len(name_list) == 1:
        name_num = name_list[0]
    else:
        name_num = ".".join(name_list[:-1])
        f_ext = ".{}".format(name_list[-1])
    # Get numbering
    name_num = name_num.split("-")
    if len(name_num) == 1:
        f_name = name_num[0]
    else:
        f_name = "-".join(name_num[:-1])
        f_number = name_num[-1]
    # Add numbering
    if not f_number:
        f_number = "-1"
    else:
        try:
            f_number_int = int(f_number)
            f_number = "-{}".format(f_number_int + 1)
        except ValueError:
            f_name = "-".join(name_num)
            f_number = "-1"
    # Format the new name
    return "{}{}{}".format(f_name, f_number, f_ext)


def copy_filefield(old_file):
    # Format the new name
    name = old_file.name
    while os.path.isfile(settings.MEDIA_ROOT + "/" + name):
        name = add_name_numbering(name)
    # Read the file to save a copy
    new_file = ContentFile(old_file.read())
    new_file.name = name
    return new_file


def copy_projects(modeladmin, request, queryset):
    # Retrieve the Projects
    for old_project in queryset:
        # Copy Project
        new_project = Project()
        new_project.title = old_project.title
        new_project.user = old_project.user
        new_project.call = None
        new_project.slug = None
        new_project.created = datetime.datetime.now()
        new_project.validation_status = 4
        new_project.funding = old_project.funding
        new_project.topic = old_project.topic
        new_project.website = old_project.website
        new_project.date_from = old_project.date_from
        new_project.date_to = old_project.date_to
        for keyword in old_project.keywords.all():
            pass #TODO: Copy AssignedKeyword set
        new_project.save()
        # Copy Public Data
        new_public_data = ProjectPublicData()
        old_public_data = old_project.public_data.all().first()
        if old_public_data:
            new_public_data.brief_description = old_public_data.brief_description
            new_public_data.challenges_description = old_public_data.challenges_description
            new_public_data.technology_description = old_public_data.technology_description
            new_public_data.objectives_description = old_public_data.objectives_description
            new_public_data.resources_description = old_public_data.resources_description
            new_public_data.implementation_start_date = old_public_data.implementation_start_date
            new_public_data.implementation_period = old_public_data.implementation_period
            new_public_data.implementation_duration = old_public_data.implementation_duration
            if old_public_data.image:
                new_public_data.image_credits = old_public_data.image_credits
                new_public_data.image = copy_filefield(old_public_data.image)
        new_public_data.project = new_project
        new_public_data.save()
        # Copy Private Data
        new_private_data = ProjectPrivateData()
        old_private_data = old_project.private_data.all().first()
        if old_private_data:
            new_private_data.description = old_private_data.description
            new_private_data.funding_programme = old_private_data.funding_programme
            new_private_data.persons = old_private_data.persons
            new_private_data.dimension = old_private_data.dimension
            if old_private_data.commitment_letter:
                new_private_data.commitment_letter = copy_filefield(old_private_data.commitment_letter)
            if old_private_data.investor_letter:
                new_private_data.investor_letter = copy_filefield(old_private_data.investor_letter)
        new_private_data.project = new_project
        new_private_data.save()
        # Copy Contact Data
        new_contact_data = ProjectContact()
        old_contact_data = old_project.contacts.all().first()
        if old_contact_data:
            new_contact_data.first_name = old_contact_data.first_name
            new_contact_data.last_name = old_contact_data.last_name
            new_contact_data.organization_name = old_contact_data.organization_name
            new_contact_data.position = old_contact_data.position
            new_contact_data.email = old_contact_data.email
            new_contact_data.telephone = old_contact_data.telephone
            new_contact_data.address = old_contact_data.address
            new_contact_data.postal_code = old_contact_data.postal_code
            new_contact_data.city = old_contact_data.city
            new_contact_data.country = old_contact_data.country
        if (new_contact_data.first_name is None):
            new_contact_data.first_name = ""
        if (new_contact_data.last_name is None):
            new_contact_data.last_name = ""
        new_contact_data.project = new_project
        new_contact_data.save()
        # Copy Project Images
        for old_image in old_project.user_images.all():
            new_image = ProjectUserImage()
            new_image.title = old_image.title
            new_image.description = old_image.description
            new_image.credits = old_image.credits
            new_image.file = copy_filefield(old_image.file)
            new_image.project = new_project
            new_image.save()


copy_projects.short_description = "Copy selected Projects"


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
                if producer.organization:
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
    filter_horizontal = ['teams', 'organizations']
    list_filter = ['validation_status', 'call', 'topic']
    list_editable = ['validation_status']
    list_display = ['title', 'created', 'updated', 'call', 'validation_status', 'topic', 'date_from', 'date_to', 'admin_link']
    actions = [export_projects_as_csv, copy_projects]




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


class CallAdmin(admin.ModelAdmin):

    model = Call


class CallAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ProjectCallAdmin.fieldsets)


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
admin.site.register(Call, CallAdminDisplayable)
admin.site.register(ProjectPage, ProjectPageAdminDisplayable)
