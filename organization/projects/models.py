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

import datetime
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.core.files.images import get_image_dimensions
from django.urls import reverse
from organization.core.models import TitledSlugged, Period,\
    Named, Titled, Description, Block, Link, Image, UserImage, File,\
    SubTitled, NamedOnly, RelatedTitle, URL, DynamicContent, Address
from organization.pages.models import Page
from organization.network.models import Person, Organization
from organization.magazine.models import Article
from organization.media.models import PlaylistRelated
from mezzanine_agenda.models import Event
from mezzanine.core.models import RichText, Displayable, Orderable, MetaData,\
    TimeStamped, RichTextField, TeamOwnable

from django.conf import settings

REPOSITORY_ACCESS_CHOICES = [
    ('public', _('public')),
    ('shared', _('shared')),
    ('private', _('private')),
]

DIMENSION_CHOICES = (
    ('startup', _('Start-up / Micro')),
    ('sme', _('SME')),
    ('large', _('Large')),
)

PROJECT_TYPE_CHOICES = [
    ('internal', ('Internal project')),
    ('external', ('National or European project')),
    ('industrial', ('Industrial project')),
]

PROJECT_STATUS_CHOICES = (
    (0, ('rejected')),
    (1, ('pending')),
    (2, ('in process')),
    (3, ('accepted')),
)

FUNDING_CHOICES = (
    ('public', ('EU / National Program')),
    ('private', ('Privately Funded'))
)


class Project(
        TitledSlugged,
        MetaData,
        TimeStamped,
        Period,
        RichText,
        TeamOwnable,
):
    # class Project(Displayable, Period, RichText, OwnableOrNot):
    """(Project description)"""

    type = models.CharField(
        ('type'),
        max_length=128,
        choices=PROJECT_TYPE_CHOICES,
        blank=True
    )
    external_id = models.CharField(
        ('external ID'),
        blank=True,
        null=True,
        max_length=128
    )
    program = models.ForeignKey(
        'ProjectProgram',
        verbose_name=('project program'),
        related_name='projects',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    program_type = models.ForeignKey(
        'ProjectProgramType',
        verbose_name=('project program type'),
        related_name='projects',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    call = models.ForeignKey(
        'ProjectCall',
        verbose_name=('project call'),
        related_name='projects',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    lead_team = models.ForeignKey(
        'organization_network.Team',
        verbose_name=('lead team'),
        related_name='leader_projects',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    lead_organization = models.ForeignKey(
        'organization_network.Organization',
        verbose_name=('lead organization'),
        related_name='leader_projects',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    teams = models.ManyToManyField(
        'organization_network.Team',
        verbose_name=('teams'),
        related_name='partner_projects',
        blank=True
    )
    organizations = models.ManyToManyField(
        'organization_network.Organization',
        verbose_name=('organizations'),
        blank=True
    )
    website = models.URLField(
        ('website'),
        max_length=512,
        blank=True
    )
    topic = models.ForeignKey(
        'ProjectTopic',
        verbose_name=('topic'),
        related_name='projects',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    referring_person = models.ManyToManyField(
        'organization_network.Person',
        verbose_name=('Referring Person'),
        related_name='projects_referring_person', blank=True
    )
    manager = models.ManyToManyField(
        'organization_network.Person',
        verbose_name=('Manager'),
        related_name='projects_manager',
        blank=True
    )
    is_archive = models.BooleanField(
        verbose_name=('Is Archive'),
        help_text='Hide project in Team Page',
        default=False
    )
    validation_status = models.IntegerField(
        ('validation status'),
        choices=PROJECT_STATUS_CHOICES,
        default=1
    )
    funding = models.CharField(
        ('funding'),
        choices=FUNDING_CHOICES,
        max_length=128,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = ('project')
        verbose_name_plural = ("projects")
        ordering = ['title', ]
        permissions = TeamOwnable.Meta.permissions

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from organization.projects.models import ProjectTopic
        ict_topic, c = ProjectTopic.objects.get_or_create(key='ICT')
        if self.topic == ict_topic:
            return reverse(
                "organization-ict-project-detail",
                kwargs={"slug": self.slug}
            )
        return reverse("organization-project-detail", kwargs={"slug": self.slug})

    def project_status(self):
        if self.date_from and self.date_to:
            if datetime.date.today() >= self.date_from and\
                    datetime.date.today() <= self.date_to:
                return ('in progress')
            elif datetime.date.today() < self.date_from and\
                    datetime.date.today() < self.date_to:
                return ('pending')
            elif datetime.date.today() > self.date_to and\
                    datetime.date.today() > self.date_to:
                return ('completed')
        else:
            return ('pending')


class ProjectTopic(Named):

    key = models.CharField(_('key'), unique=True, max_length=128)
    parent = models.ForeignKey(
        'ProjectTopic',
        verbose_name=_('parent topic'),
        related_name='topics',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _('project topic')
        verbose_name_plural = _("project topics")
        ordering = ['key', ]

    def __str__(self):
        if self.parent:
            return ' - '.join((self.parent.name, self.name))
        else:
            return self.name


class ProjectProgram(Named):

    class Meta:
        verbose_name = _('program')
        verbose_name_plural = _("programs")
        ordering = ['name', ]


class ProjectProgramType(Named):

    class Meta:
        verbose_name = _('program type')
        verbose_name_plural = _("program types")
        ordering = ['name', ]


class ProjectWorkPackage(Titled, Description, Period):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='work_packages',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    number = models.IntegerField(_('number'))
    lead_organization = models.ForeignKey(
        'organization_network.Organization',
        verbose_name=_('lead organization'),
        related_name='leader_work_packages',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _('work package')
        verbose_name_plural = _("work packages")
        ordering = ['number', ]


class ProjectPlaylist(PlaylistRelated):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='playlists',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectLink(Link):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='links',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectImage(Image):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectUserImage(UserImage):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='user_images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectFile(File):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='files',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectBlock(Block):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='blocks',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectTopicPage(Page, SubTitled):

    project_topic = models.ForeignKey(
        'ProjectTopic',
        verbose_name=_('project topic'),
        related_name="pages",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    display_navbar = models.BooleanField(default=True)
    displayed_in_navbars = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('project topic page')
        verbose_name_plural = _("project topic pages")


class ProjectCall(Displayable, Period, RichText, NamedOnly):

    project_form_content = RichTextField(
        _("Project form content"),
        blank=True,
        null=True
    )
    residency_form_content = RichTextField(
        _("Residency form content"),
        blank=True,
        null=True
    )
    producer_form_content = RichTextField(
        _("Producer form content"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('project call')
        verbose_name_plural = _("project calls")
        ordering = ['title', ]

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
        except Exception:
            pass
        return True


class ProjectCallBlock(Block):

    call = models.ForeignKey(
        'ProjectCall',
        verbose_name=_('project call'),
        related_name='blocks',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectCallImage(Image):

    call = models.ForeignKey(
        'ProjectCall',
        verbose_name=_('project call'),
        related_name='images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectCallFile(File):

    call = models.ForeignKey(
        'ProjectCall',
        verbose_name=_('project call'),
        related_name='files',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectCallLink(Link):

    call = models.ForeignKey(
        'ProjectCall',
        verbose_name=_('project call'),
        related_name='links',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectDemo(Displayable, RichText, URL):

    project = models.ForeignKey(
        'Project',
        verbose_name=_('project'),
        related_name='demos',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    authors = models.ManyToManyField(
        Person,
        verbose_name=_('authors'),
        related_name='demos',
        blank=True
    )
    repository = models.ForeignKey(
        'Repository',
        verbose_name=_('repository'),
        related_name='demos',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    build_commands = models.TextField(
        _('build commands'),
        blank=True
    )
    directory = models.CharField(
        _('directory'),
        max_length=256,
        blank=True,
        null=True,
        help_text='Relative directory in repository'
    )

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


class Repository(Named):

    system = models.ForeignKey(
        'RepositorySystem',
        verbose_name=_('system'),
        related_name='repositories',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    access = models.CharField(
        _('access rights'),
        max_length=64,
        choices=REPOSITORY_ACCESS_CHOICES,
        default='private'
    )
    branch = models.CharField(
        _('branch'),
        max_length=32,
        default='master'
    )
    url = models.CharField(
        _('URL'),
        max_length=256,
        help_text='http(s) or ssh'
    )

    class Meta:
        verbose_name = _('repository')
        verbose_name_plural = _("repositories")

    def save(self, *args, **kwargs):
        super(Repository, self).save(args, kwargs)
        os.path.exists(self.directory)
        if not os.path.exists(self.directory):
            self.clone()
        self.checkout()

    @property
    def directory(self):
        dir_name = self.url.split('/')[-1].split('.')[0]
        return settings.PROJECT_DEMOS_DIR + dir_name

    def clone(self):
        os.chdir(settings.PROJECT_DEMOS_DIR)
        os.system(' '.join((self.system.clone_command, self.url)))

    def pull(self):
        os.chdir(self.directory)
        os.system(' '.join((self.system.pull_command, self.branch)))

    def checkout(self):
        os.chdir(self.directory)
        os.system(' '.join((self.system.checkout_command, self.branch)))


class RepositorySystem(Named):

    clone_command = models.CharField(_('clone command'), max_length=256)
    pull_command = models.CharField(_('pull command'), max_length=256)
    checkout_command = models.CharField(_('checkout command'), max_length=256)
    branch_command = models.CharField(_('branch command'), max_length=256)

    class Meta:
        verbose_name = _('repository system')
        verbose_name_plural = _("repository systems")


class ProjectRelatedTitle(RelatedTitle):

    project = models.OneToOneField(
        Project,
        verbose_name=_('project'),
        related_name='related_title',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _("related title")
        order_with_respect_to = "project"


class DynamicContentProject(DynamicContent, Orderable):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='dynamic_content_project',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Dynamic Content Project'


class DynamicMultimediaProject(DynamicContent, Orderable):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='dynamic_multimedia',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Multimedia'


class ProjectBlogPage(Displayable, RichText):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='blog_pages',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    login_required_content = RichTextField(_("Login required content"), null=True)

    class Meta:
        verbose_name = 'Project blog page'
        verbose_name_plural = 'Project blog pages'

    def get_absolute_url(self):
        return reverse(
            "organization-project-blogpage-detail",
            kwargs={"slug": self.slug}
        )


class ProjectPublicData(models.Model):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='public_data',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    brief_description = models.CharField(
        _('brief description'),
        max_length=110,
        help_text="Brief description of the technology/challenges"
        " faced by the project (110 characters max)."
    )
    challenges_description = models.TextField(
        _('challenges description'),
        help_text="Description of the project technology to be made"
        " available to artist + challenges it produces (100 words - must include"
        " the elements to be made available to the artist with sufficient functional"
        " and implementation details for enabling him/her to "
        "elaborate a technical approach)."
    )
    technology_description = models.TextField(
        _('technology description'),
        help_text="Must include the elements to be made available to the artist with"
        " sufficient functional and implementation details for enabling him/her to"
        " elaborate his/her technical approach (100-200 words)."
    )
    objectives_description = models.TextField(
        _('objectives description'),
        help_text="What the project is looking to gain from the collaboration"
        " and what kind of artist would be suitable (100 – 150 words)."
    )
    resources_description = models.TextField(
        _('resource description'),
        help_text="Resources available to the artist -- e.g. office facility, studio"
        " facility, technical equipment, internet connection, laboratory, and periods"
        " of availability for artistic production, staff possibly allocated to the"
        " project, available budget for travel, consumables and "
        "equipment, etc... (50 – 100 words)."
    )
    implementation_start_date = models.DateField(
        _('residency start date'),
        help_text="Possible period for the implementation of the residency"
        " (must be within the period of the project implementation workplan)"
        " (MM/DD/YYYY)"
    )
    implementation_period = models.DateField(
        _('period for direct cooperation'),
        blank=False,
        null=True,
        help_text="Possible period for direct cooperation with the"
        " artist (must be within the period of the project "
        "implementation workplan) (MM/DD/YYYY)"
    )
    implementation_duration = models.CharField(
        _('residency duration'),
        max_length=128, help_text="Possible duration of implementation in"
        " months (must be part of the project implementation workplan) (months)"
    )
    image = models.FileField(
        _("Image"),
        max_length=1024,
        upload_to="user/images/%Y/%m/%d/",
        help_text="Representing the project"
    )
    image_credits = models.CharField(
        _('Image credits'),
        max_length=256,
        null=True
    )

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
        except Exception:
            panoramic = True
        return panoramic


class ProjectPrivateData(models.Model):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='private_data',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    description = models.TextField(
        _('project description'),
        help_text="(500 - 1000 words)"
    )
    funding_programme = models.CharField(
        _('funding programme'),
        max_length=512,
        blank=False,
        null=True,
        help_text="Designation of EU/National Funding Programme"
    )
    commitment_letter = models.FileField(
        _("letter of commitment by the project coordinator"),
        max_length=1024,
        upload_to="user/documents/%Y/%m/%d/",
        help_text=mark_safe(
            'Written on behalf of the whole project consortium'
            ', this letter will commit in implementing the collaboration'
            ' of a residency application selected by the VERTIGO jury, on'
            ' the conditions set by the project (in annex of letter: synthesis'
            ' of all related information entered by project).<br>Please '
            '<a href="http://vertigo.starts.eu/media/uploads/vertigo%20starts/CALL/vertigo_loc_v3.rtf">'  # noqa: E501
            'download and use the template letter.</a>'
        )
    )
    investor_letter = models.FileField(
        _("letter of recommendations from investor (e.g VC)"),
        max_length=1024,
        blank=False,
        null=True,
        upload_to="user/documents/%Y/%m/%d/",
        help_text="If the organisation is a Start-Up or micro enterprise"
        " (less than 3 years and/or less than 10 staff members), the presentation"
        " of letter of recommendation from an investor is mandatory"
        " to apply to this call."
    )
    persons = models.CharField(
        _('persons'),
        max_length=512,
        help_text="First name and last name of the persons from organization /"
        " project who will be part preliminary of the project team"
        " (separated by a comma)"
    )
    dimension = models.CharField(
        _('dimension'),
        max_length=128,
        choices=DIMENSION_CHOICES,
        blank=False,
        null=True
    )

    class Meta:
        verbose_name = 'Project private data'
        verbose_name_plural = 'Project private data'


class ProjectContact(Person):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='contacts',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    organization_name = models.CharField(
        _('organization name'),
        blank=True,
        null=True,
        max_length=128
    )
    position = models.CharField(_('position'), blank=True, null=True, max_length=128)

    class Meta:
        verbose_name = 'Project contact'
        verbose_name_plural = 'Project contacts'


class ProjectResidency(Displayable, Period, Address, RichText):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='residencies',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    artist = models.ForeignKey(
        Person,
        verbose_name=_('artist'),
        related_name='residencies',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    validated = models.BooleanField(default=False)
    producer_commitment = models.TextField(_('producer commitment'), help_text="")

    @property
    def articles(self):
        # TODO: Any way to avoid magic number in status filter?
        articles = Article.objects.filter(residencies__residency=self)\
            .filter(status=2)\
            .filter(publish_date__lte=datetime.date.today())\
            .order_by("-publish_date")
        return articles

    @property
    def events(self):
        # TODO: Any way to avoid magic number in status filter?
        events = Event.objects.filter(residencies__residency=self)\
            .filter(status=2)\
            .filter(publish_date__lte=datetime.date.today())\
            .order_by("-publish_date")
        return events

    class Meta:
        verbose_name = 'Project residency'
        verbose_name_plural = 'Project residencies'

    def get_absolute_url(self):
        call_slug = ''
        if self.project:
            if self.project.call:
                call_slug = self.project.call.slug
        return reverse(
            "organization-residency-detail",
            kwargs={"call_slug": call_slug, "slug": self.slug}
        )


class ProjectResidencyProducer(models.Model):

    residency = models.ForeignKey(
        ProjectResidency,
        verbose_name=_('residency'),
        related_name='producers',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    organization = models.ForeignKey(
        Organization,
        verbose_name=_('producer'),
        related_name='residencies',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectResidencyFile(File):

    residency = models.ForeignKey(
        ProjectResidency,
        verbose_name=_('project residency file'),
        related_name='files',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectResidencyImage(Image):

    residency = models.ForeignKey(
        ProjectResidency,
        verbose_name=_('project residency image'),
        related_name='images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectResidencyUserImage(UserImage):

    residency = models.ForeignKey(
        ProjectResidency,
        verbose_name=_('project residency user image'),
        related_name='user_images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectResidencyArticle(models.Model):

    residency = models.ForeignKey(
        ProjectResidency,
        verbose_name=_('residency'),
        related_name='residency_articles',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    article = models.ForeignKey(
        Article,
        verbose_name=_('article'),
        related_name='residencies',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectResidencyEvent(models.Model):

    residency = models.ForeignKey(
        ProjectResidency,
        verbose_name=_('residency'),
        related_name='residency_events',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    event = models.ForeignKey(
        Event,
        verbose_name=_('event'),
        related_name='residencies',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectPage(Displayable, RichText, TeamOwnable):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='pages',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    display_navbar = models.BooleanField(default=True)
    displayed_in_navbars = models.BooleanField(default=True)

    @property
    def is_archive(self):
        if self.project:
            return self.project.is_archive

    def get_absolute_url(self):
        return reverse(
            "organization-project-projectpage-detail",
            kwargs={'slug': self.slug}
        )

    class Meta:
        permissions = TeamOwnable.Meta.permissions


class ProjectPageImage(Image):

    project_page = models.ForeignKey(
        ProjectPage,
        verbose_name=_('project page'),
        related_name='images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectPageBlock(Block):

    project_page = models.ForeignKey(
        ProjectPage,
        verbose_name=_('project page'),
        related_name='blocks',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class DynamicContentProjectPage(DynamicContent, Orderable):

    project_page = models.ForeignKey(
        ProjectPage,
        verbose_name=_('project page'),
        related_name='dynamic_content_project_pages',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Dynamic Content Project Page'
