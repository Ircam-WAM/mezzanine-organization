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

from __future__ import unicode_literals
import datetime
import os
import copy

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.conf import settings

from mezzanine.core.models import RichText, Displayable, Slugged, Orderable
from django.core.files.images import get_image_dimensions

from organization.core.models import *
from organization.pages.models import *
from organization.network.models import *
from organization.magazine.models import Article
from mezzanine_agenda.models import *

from skosxl.models import Concept


PROJECT_TYPE_CHOICES = [
    ('internal', _('internal')),
    ('external', _('external')),
]
if settings.PROJECT_TYPE_CHOICES:
    PROJECT_TYPE_CHOICES.extend(settings.PROJECT_TYPE_CHOICES)

REPOSITORY_ACCESS_CHOICES = [
    ('public', _('public')),
    ('shared', _('shared')),
    ('private', _('private')),
]

REPOSITORY_VENDORS = [
    ('gitlab', _('Gitlab')),
]

PROJECT_STATUS_CHOICES = (
    (0, _('rejected')),
    (1, _('pending')),
    (2, _('in process')),
    (3, _('accepted')),
)

DIMENSION_CHOICES = (
    ('startup', _('Start-up / Micro')),
    ('sme', _('SME')),
    ('large', _('Large')),
)

FUNDING_CHOICES = (
    ('public', _('EU / National Program')),
    ('private', _('Privately Funded'))
)


class Project(Displayable, Period, RichText, OwnableOrNot):
    """(Project description)"""

    type = models.CharField(_('type'), max_length=128, choices=PROJECT_TYPE_CHOICES)
    external_id = models.CharField(_('external ID'), blank=True, null=True, max_length=128)
    program = models.ForeignKey('ProjectProgram', verbose_name=_('project program'), related_name='projects', blank=True, null=True, on_delete=models.SET_NULL)
    program_type = models.ForeignKey('ProjectProgramType', verbose_name=_('project program type'), related_name='projects', blank=True, null=True, on_delete=models.SET_NULL)
    call = models.ForeignKey('ProjectCall', verbose_name=_('project call'), related_name='projects', blank=True, null=True, on_delete=models.SET_NULL)
    lead_team = models.ForeignKey('organization-network.Team', verbose_name=_('lead team'), related_name='leader_projects', blank=True, null=True, on_delete=models.SET_NULL)
    lead_organization = models.ForeignKey('organization-network.Organization', verbose_name=_('lead organization'), related_name='leader_projects', blank=True, null=True, on_delete=models.SET_NULL)
    teams = models.ManyToManyField('organization-network.Team', verbose_name=_('teams'), related_name='partner_projects', blank=True)
    organizations = models.ManyToManyField('organization-network.Organization', verbose_name=_('organizations'), blank=True)
    website = models.URLField(_('website'), max_length=512, blank=True)
    topic = models.ForeignKey('ProjectTopic', verbose_name=_('topic'), related_name='projects', blank=True, null=True, on_delete=models.SET_NULL)
    topics = models.ManyToManyField('ProjectTopic', verbose_name=_('topics'), related_name='project_topics', blank=True)
    referring_person = models.ManyToManyField('organization-network.Person', verbose_name=_('Referring Person'), related_name='projects_referring_person', blank=True)
    manager =  models.ManyToManyField('organization-network.Person', verbose_name=_('Manager'), related_name='projects_manager', blank=True)
    is_archive = models.BooleanField(verbose_name=_('Is Archive'), help_text='Hide project in Team Page', default=False)
    is_private = models.BooleanField(verbose_name=_('Is private'), help_text='If the project is private, permissions will be enforced. Else, the project is considered public and they will be omitted.', default=False)
    validation_status = models.IntegerField(_('validation status'), choices=PROJECT_STATUS_CHOICES, default=1)
    funding = models.CharField(_('funding'), choices=FUNDING_CHOICES, max_length=128, blank=True, null=True)
    concepts = models.ManyToManyField('skosxl.Concept', verbose_name=_('concepts'), blank=True)

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _("projects")
        # ordering = ['-date_from', '-date_to']
        ordering = ['title', ]
        permissions = (
            ('view_project', 'Can view project'),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        ict_topic, c = ProjectTopic.objects.get_or_create(key='ICT')
        if self.topic == ict_topic:
            return reverse("organization-ict-project-detail", kwargs={"slug": self.slug})
        return reverse("organization-project-detail", kwargs={"slug": self.slug})

    def project_status(self):
        if self.date_from and self.date_to:
            if datetime.date.today() >= self.date_from and datetime.date.today() <= self.date_to:
                return _('in progress')
            elif datetime.date.today() < self.date_from and datetime.date.today() < self.date_to:
                return _('pending')
            elif datetime.date.today() > self.date_to and datetime.date.today() > self.date_to:
                return _('completed')
        else:
            return _('pending')

    @property
    def download_urls(self):

        ret = []  # TODO: must set a schema for simple, clear format in the templates
                  #       example: { version, platform, url, featured } or even more abstract

        direct_url = self.get_link('download')  # First we try to get the "download" link type
        if direct_url:
            ret.append({
                'url': direct_url.url,
                'featured': True
            })

        from repository import repository as r
        # If no 'download' link is found, fallback to the latest tag from the first repository
        # TODO: what about multiple repositories?
        for i, pr in enumerate(self.project_repositories.all()):
            ret.append({
                'url': r.Repository(pr.repository.url, pr.repository.vendor).get_archive_url(),
                'featured': (not direct_url and i == 0)  # Only the first repository URL is featured,
                                                         # if and only if no direct link has been set up
            })
        return ret

    @property
    def documentation_url(self):
        return self.get_link('documentation')

    @property
    def repositories(self):
        return self.get_repositories()

    @property
    def discussion_rooms(self):
        return self.get_discussion_rooms()

    def get_link(self, link_type_slug=None):
        ret = None
        link_type = LinkType.objects.filter(slug=link_type_slug)
        urls = self.links.filter(link_type=link_type)
        if len(urls) > 0:
            ret = urls.first()
        return ret

    def get_discussion_rooms(self):

        from discussion import discussion as d

        rooms_urls = []
        discussion_rooms = []

        # Room URLs are stored as ProjectLink's
        discussion_link_type = LinkType.objects.get(slug="discussion")
        for project_link in self.links.filter(link_type=discussion_link_type):
            rooms_urls.append(project_link.url)

        for room_url in rooms_urls:
            tmp = {}
            tmp['url'] = room_url
            tmp['summary'] = d.Discussion(room_url, 'discourse').get_summary()
            discussion_rooms.append(tmp)

        return discussion_rooms

    def get_repositories(self):

        from repository import repository as r

        repositories = []

        for project_repository in self.project_repositories.all():
            tmp = {}
            repository = project_repository.repository
            tmp['url'] = repository.url
            tmp['readme_html'] = r.Repository(repository.url, 'gitlab').get_readme()
            tmp['summary'] = r.Repository(repository.url, 'gitlab').get_summary()
            repositories.append(tmp)

        return repositories

    def get_contributors(self):

        # NOTE: will need a bigass cache because it fetch resources from everywhere

        # Project contributors are sourced from:
        # - Repositories (commits authors and members)
        # - Discussion rooms (participants)
        # - Forum project members

        from repository import repository as r
        from discussion import discussion as d
        import forum_utils  # SMELL: makes the method forum-specific, move logic elsewhere?

        CONTRIBUTORS_SOURCES = [
            'repository_commits_contributors',
            'repository_members',
            'repository_issues_contributors',
            'forum_project_members',
            'discussion_participants'
        ]

        # Not actually enforced. For info only.
        CONTRIBUTOR_SCHEMA = {
            'first_name': None,  # Optional
            'last_name': None,   # Optional
            'username': None,    # Optional
            'name': None,        # Mandatory. Composed name or username depending on source
            'email': None,       # Optional
            'avatar_url': None,  # Optional. Getting it from Ircam OAuth server if email matches
            'source': None,      # Mandatory. One of CONTRIBUTORS_SOURCES
            'extra_data': {}     # Optional
        }

        contributors = []  # Holds all the contributors from all the sources

        from pprint import pprint

        # Getting each source
        for source in CONTRIBUTORS_SOURCES:

            # Commits and issues contributors
            if source in ['repository_commits_contributors', 'repository_issues_contributors', 'repository_members']:

                # For each project repository...
                for project_repository in self.project_repositories.all():

                    repository_contributors = []
                    repository = project_repository.repository

                    repository_instance = r.Repository(repository.url, 'gitlab')

                    if source == 'repository_commits_contributors':
                        repository_contributors = repository_instance.get_commits_contributors()
                    elif source == 'repository_issues_contributors':
                        repository_contributors = repository_instance.get_issues_contributors()
                    elif source == 'repository_members':
                        repository_contributors = repository_instance.get_members()

                    # Augmenting the contributors data with source
                    for c in repository_contributors:

                        tmp = copy.copy(c)
                        #tmp.pop('email', None)  # We don't want the email to be visible
                        tmp['source'] = source  # IDEA: include which repository?
                        if c['email']:
                            tmp['oauth_id'] = forum_utils.get_oauth_id(email=c['email'])
                        else:
                            tmp['oauth_id'] = None
                        # TODO: add avatar URL
                        
                        contributors.append(tmp)

        # NOTE: there may be duplicates, leaving the function caller the care to deduplicate it
        # (duplicates can be used to determine a count, e.g. user posted X issues, etc.)
        # If deduplicating it, the OAuth ID is the only really unique value to be trusted

        return contributors


class ProjectTopic(Named):

    key = models.CharField(_('key'), unique=True, max_length=128)
    parent = models.ForeignKey('ProjectTopic', verbose_name=_('parent topic'), related_name='topics', blank=True, null=True)

    class Meta:
        verbose_name = _('project topic')
        verbose_name_plural = _("project topics")
        ordering = ['key',]

    def __str__(self):
        if self.parent:
            return ' - '.join((self.parent.name, self.name))
        else:
            return self.name


class ProjectProgram(Named):

    class Meta:
        verbose_name = _('program')
        verbose_name_plural = _("programs")
        ordering = ['name',]


class ProjectProgramType(Named):

    class Meta:
        verbose_name = _('program type')
        verbose_name_plural = _("program types")
        ordering = ['name',]


class ProjectWorkPackage(Titled, Period):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='work_packages')
    number = models.IntegerField(_('number'))
    lead_organization = models.ForeignKey('organization-network.Organization', verbose_name=_('lead organization'), related_name='leader_work_packages', blank=True, null=True)

    class Meta:
        verbose_name = _('work package')
        verbose_name_plural = _("work packages")
        ordering = ['number',]


class ProjectPlaylist(PlaylistRelated):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='playlists', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectLink(Link):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectImage(Image):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectUserImage(UserImage):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='user_images', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectFile(File):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='files', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectBlock(Block):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectTopicPage(Page, SubTitled):

    project_topic = models.ForeignKey('ProjectTopic', verbose_name=_('project topic'), related_name="pages", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('project topic page')
        verbose_name_plural = _("project topic pages")


class ProjectCall(Displayable, Period, RichText, NamedOnly):

    project_form_content = RichTextField(_("Project form content"), blank=True, null=True)
    residency_form_content = RichTextField(_("Residency form content"), blank=True, null=True)
    producer_form_content = RichTextField(_("Producer form content"), blank=True, null=True)

    class Meta:
        verbose_name = _('project call')
        verbose_name_plural = _("project calls")
        ordering = ['title',]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("organization-call-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.name and self.title:
            self.name = self.title
        if not self.title and self.name:
            self.title = self.name
        super(ProjectCall, self).save(args, kwargs)

    @property
    def is_closed(self):
        """Return if the current date between 'from' and 'to' dates."""
        try:
            current_date = datetime.date.today()
            if current_date >= self.date_from and current_date <= self.date_to:
                return False
        except:
            pass
        return True


class ProjectCallBlock(Block):

    call = models.ForeignKey('ProjectCall', verbose_name=_('project call blocks'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectCallImage(Image):

    call = models.ForeignKey('ProjectCall', verbose_name=_('project call image'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectCallFile(File):

    call = models.ForeignKey('ProjectCall', verbose_name=_('project call file'), related_name='files', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectCallLink(Link):

    call = models.ForeignKey('ProjectCall', verbose_name=_('project call link'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectDemo(Displayable, RichText, URL):

    project = models.ForeignKey('Project', verbose_name=_('project'), related_name='demos', blank=True, null=True, on_delete=models.SET_NULL)
    authors = models.ManyToManyField(Person, verbose_name=_('authors'), related_name='demos', blank=True)
    repository = models.ForeignKey('Repository', verbose_name=_('repository'), related_name='demos', blank=True, null=True, on_delete=models.SET_NULL)
    build_commands = models.TextField(_('build commands'), blank=True)
    directory = models.CharField(_('directory'), max_length=256, blank=True, null=True, help_text='Relative directory in repository')

    class Meta:
        verbose_name = _('project demo')
        verbose_name_plural = _("project demos")

    def get_absolute_url(self):
        return reverse("organization-project-demo-detail", kwargs={"slug": self.slug})

    @property
    def relative_url(self):
        path = self.repository.directory.replace(settings.MEDIA_ROOT, '')
        return settings.MEDIA_URL + path + os.sep + self.directory + '/index.html'

    def build(self):
        os.chdir(self.repository.directory)
        for command in self.build_commands.split('\n'):
            os.system(command)

    def save(self, *args, **kwargs):
        super(ProjectDemo, self).save(args, kwargs)
        if self.repository:
            self.build()


class Repository(models.Model):

    system = models.ForeignKey('RepositorySystem', verbose_name=_('system'), related_name='repositories')
    url = models.CharField(_('URL'), max_length=256, help_text='http(s)')
    vendor = models.CharField(_('vendor'), max_length=64, choices=REPOSITORY_VENDORS, default='gitlab')

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = _('repository')
        verbose_name_plural = _("repositories")


class RepositorySystem(Named):

    class Meta:
        verbose_name = _('repository system')
        verbose_name_plural = _("repository systems")


class ProjectRepository(models.Model):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='project_repositories', blank=True, null=True, on_delete=models.SET_NULL)
    repository = models.ForeignKey(Repository, verbose_name=_('repository'), related_name='project_repositories', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.repository.url

    class Meta:
        verbose_name = _('project repository')
        verbose_name_plural = _("project repositories")

class ProjectRelatedTitle(RelatedTitle):

    project = models.OneToOneField(Project, verbose_name=_('project'), related_name='related_title', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("related title")
        order_with_respect_to = "project"


class DynamicContentProject(DynamicContent, Orderable):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='dynamic_content_project', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Linked Project'


class ProjectBlogPage(Displayable, RichText):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='blog_pages', blank=True, null=True, on_delete=models.SET_NULL)
    login_required_content = RichTextField(_("Login required content"), null=True)

    class Meta:
        verbose_name = 'Project blog page'
        verbose_name_plural = 'Project blog pages'

    def get_absolute_url(self):
        return reverse("organization-project-blogpage-detail", kwargs={"slug": self.slug})


class ProjectPublicData(models.Model):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='public_data', blank=True, null=True, on_delete=models.SET_NULL)

    brief_description = models.CharField(_('brief description'), max_length=110, help_text="Brief description of the technology/challenges faced by the project (110 characters max).")
    challenges_description = models.TextField(_('challenges description'), help_text="Description of the project technology to be made available to artist + challenges it produces (100 words - must include the elements to be made available to the artist with sufficient functional and implementation details for enabling him/her to elaborate a technical approach).")
    technology_description = models.TextField(_('technology description'), help_text="Must include the elements to be made available to the artist with sufficient functional and implementation details for enabling him/her to elaborate his/her technical approach (100-200 words).")
    objectives_description = models.TextField(_('objectives description'), help_text="What the project is looking to gain from the collaboration and what kind of artist would be suitable (100 – 150 words).")
    resources_description = models.TextField(_('resource description'), help_text="Resources available to the artist -- e.g. office facility, studio facility, technical equipment, internet connection, laboratory, and periods of availability for artistic production, staff possibly allocated to the project, available budget for travel, consumables and equipment, etc... (50 – 100 words).")
    implementation_start_date = models.DateField(_('residency start date'), help_text="Possible period for the implementation of the residency (must be within the period of the project implementation workplan) (MM/DD/YYYY)")
    implementation_period = models.DateField(_('period for direct cooperation'), blank=False, null=True, help_text="Possible period for direct cooperation with the artist (must be within the period of the project implementation workplan) (MM/DD/YYYY)")
    implementation_duration = models.CharField(_('residency duration'), max_length=128, help_text="Possible duration of implementation in months (must be part of the project implementation workplan) (months)")
    image = models.FileField(_("Image"), max_length=1024, upload_to="user/images/%Y/%m/%d/", help_text="Representing the project")
    image_credits = models.CharField(_('Image credits'), max_length=256, null=True)

    class Meta:
        verbose_name = 'Project public data'
        verbose_name_plural = 'Project public data'

    @property
    def image_is_panoramic(self):
        """Return True if the image has a 3:2 ratio or bigger."""
        try:
            img_width, img_height = get_image_dimensions(self.image.file)
            # Images go in a 427x286 box -> 3:2 ratio
            if (img_width / img_height) >= 1.5:
                panoramic = True
            else:
                panoramic = False
        except:
            panoramic = True
        return panoramic


class ProjectPrivateData(models.Model):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='private_data', blank=True, null=True, on_delete=models.SET_NULL)

    description = models.TextField(_('project description'), help_text="(500 - 1000 words)")
    funding_programme = models.CharField(_('funding programme'), max_length=512, blank=False, null=True, help_text="Designation of EU/National Funding Programme")
    commitment_letter = models.FileField(_("letter of commitment by the project coordinator"), max_length=1024, upload_to="user/documents/%Y/%m/%d/", help_text=mark_safe('Written on behalf of the whole project consortium, this letter will commit in implementing the collaboration of a residency application selected by the VERTIGO jury, on the conditions set by the project (in annex of letter: synthesis of all related information entered by project).<br>Please <a href="http://vertigo.starts.eu/media/uploads/vertigo%20starts/CALL/vertigo_loc_v3.rtf">download and use the template letter.</a>'))
    investor_letter = models.FileField(_("letter of recommendations from investor (e.g VC)"), max_length=1024 , blank=False, null=True, upload_to="user/documents/%Y/%m/%d/", help_text="If the organisation is a Start-Up or micro enterprise (less than 3 years and/or less than 10 staff members), the presentation of letter of recommendation from an investor is mandatory to apply to this call.")
    persons = models.CharField(_('persons'), max_length=512, help_text="First name and last name of the persons from organization / project who will be part preliminary of the project team (separated by a comma)")
    dimension = models.CharField(_('dimension'), max_length=128, choices=DIMENSION_CHOICES, blank=False, null=True)

    class Meta:
        verbose_name = 'Project private data'
        verbose_name_plural = 'Project private data'


class ProjectContact(Person):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='contacts', blank=True, null=True, on_delete=models.SET_NULL)
    organization_name = models.CharField(_('organization name'), blank=True, null=True, max_length=128)
    position = models.CharField(_('position'), blank=True, null=True, max_length=128)

    class Meta:
        verbose_name = 'Project contact'
        verbose_name_plural = 'Project contacts'


class ProjectResidency(Displayable, Period, Address, RichText):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='residencies', blank=True, null=True, on_delete=models.SET_NULL)
    artist = models.ForeignKey(Person, verbose_name=_('artist'), related_name='residencies', blank=True, null=True, on_delete=models.SET_NULL)
    validated = models.BooleanField(default=False)
    producer_commitment = models.TextField(_('producer commitment'), help_text="")
    mappable_location = models.CharField(max_length=128, blank=True, null=True, help_text="This address will be used to calculate latitude and longitude. Leave blank and set Latitude and Longitude to specify the location yourself, or leave all three blank to auto-fill from the Location field.")
    lat = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="Latitude", help_text="Calculated automatically if mappable location is set.")
    lon = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="Longitude", help_text="Calculated automatically if mappable location is set.")

    @property
    def articles(self):
        #TODO: Any way to avoid magic number in status filter?
        articles = Article.objects.filter(residencies__residency=self).filter(status=2).filter(publish_date__lte=datetime.date.today()).order_by("-publish_date")
        return articles


    @property
    def events(self):
        #TODO: Any way to avoid magic number in status filter?
        events = Event.objects.filter(residencies__residency=self).filter(status=2).filter(publish_date__lte=datetime.date.today()).order_by("-publish_date")
        return events


    class Meta:
        verbose_name = 'Project residency'
        verbose_name_plural = 'Project residencies'

    def get_absolute_url(self):
        return reverse("organization-residency-detail", kwargs={"call_slug": self.project.call.slug, "slug": self.slug})

    def clean(self):
        """
        Validate set/validate mappable_location, longitude and latitude.
        """
        super(ProjectResidency, self).clean()

        if self.lat and not self.lon:
            raise ValidationError("Longitude required if specifying latitude.")

        if self.lon and not self.lat:
            raise ValidationError("Latitude required if specifying longitude.")

        if not (self.lat and self.lon) and not self.mappable_location:
            if self.address:
                self.mappable_location = self.address.replace("\n"," ").replace('\r', ' ') + ", " + self.postal_code + " " + self.city

        if self.mappable_location and not (self.lat and self.lon): #location should always override lat/long if set
            g = GoogleMaps(domain=settings.EVENT_GOOGLE_MAPS_DOMAIN)
            try:
                mappable_location, (lat, lon) = g.geocode(self.mappable_location)
            except GeocoderQueryError as e:
                raise ValidationError("The mappable location you specified could not be found on {service}: \"{error}\" Try changing the mappable location, removing any business names, or leaving mappable location blank and using coordinates from getlatlon.com.".format(service="Google Maps", error=e.message))
            except ValueError as e:
                raise ValidationError("The mappable location you specified could not be found on {service}: \"{error}\" Try changing the mappable location, removing any business names, or leaving mappable location blank and using coordinates from getlatlon.com.".format(service="Google Maps", error=e.message))
            except TypeError as e:
                raise ValidationError("The mappable location you specified could not be found. Try changing the mappable location, removing any business names, or leaving mappable location blank and using coordinates from getlatlon.com.")
            self.mappable_location = mappable_location
            self.lat = lat
            self.lon = lon


class ProjectResidencyProducer(models.Model):

    residency = models.ForeignKey(ProjectResidency, verbose_name=_('residency'), related_name='producers', blank=True, null=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(Organization, verbose_name=_('producer'), related_name='residencies', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectResidencyFile(File):

    residency = models.ForeignKey(ProjectResidency, verbose_name=_('project residency file'), related_name='files', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectResidencyImage(Image):

    residency = models.ForeignKey(ProjectResidency, verbose_name=_('project residency image'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectResidencyUserImage(UserImage):

    residency = models.ForeignKey(ProjectResidency, verbose_name=_('project residency user image'), related_name='user_images', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectResidencyArticle(models.Model):

    residency = models.ForeignKey(ProjectResidency, verbose_name=_('residency'), related_name='residency_articles', blank=True, null=True, on_delete=models.SET_NULL)
    article = models.ForeignKey(Article, verbose_name=_('article'), related_name='residencies', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectResidencyEvent(models.Model):

    residency = models.ForeignKey(ProjectResidency, verbose_name=_('residency'), related_name='residency_events', blank=True, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='residencies', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectCollection(Displayable):

    def get_absolute_url(self):
        return reverse("organization-project-collection-detail", kwargs={"slug": self.slug})


class ProjectCollectionImage(Image):

    collection = models.ForeignKey(ProjectCollection, verbose_name=_('collection'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)


class Pivot_Project_ProjectCollection(DynamicContent, Orderable):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='collections_pivot', blank=True, null=True, on_delete=models.CASCADE)
    collection = models.ForeignKey(ProjectCollection, verbose_name=_('collection'), related_name='projects_pivot', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Dynamic Collection Project'


class Pivot_ProjectTopic_Article(DynamicContent, Orderable):

    project_topic = models.ForeignKey(ProjectTopic, verbose_name=_('project topic'), related_name='articles_pivot', blank=True, null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name=_('article'), related_name='project_topics_pivot', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_topic.__str__()

    class Meta:
        verbose_name = 'Project Topic'