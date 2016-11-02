from __future__ import unicode_literals
import datetime
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from mezzanine.core.models import RichText, Displayable, Slugged, Orderable

from organization.core.models import *
from organization.pages.models import *


PROJECT_TYPE_CHOICES = [
    ('internal', _('internal')),
    ('external', _('external')),
]

ACCESS_CHOICES = [
    ('public', _('public')),
    ('shared', _('shared')),
    ('private', _('private')),
]


class Project(Displayable, Period, RichText):
    """(Project description)"""

    type = models.CharField(_('type'), max_length=128, choices=PROJECT_TYPE_CHOICES)
    program = models.ForeignKey('ProjectProgram', verbose_name=_('project program'), related_name='projects', blank=True, null=True, on_delete=models.SET_NULL)
    program_type = models.ForeignKey('ProjectProgramType', verbose_name=_('project program type'), related_name='projects', blank=True, null=True, on_delete=models.SET_NULL)
    lead_team = models.ForeignKey('organization-network.Team', verbose_name=_('lead team'), related_name='leader_projects', blank=True, null=True)
    lead_organization = models.ForeignKey('organization-network.Organization', verbose_name=_('lead organization'), related_name='leader_projects', blank=True, null=True)
    teams = models.ManyToManyField('organization-network.Team', verbose_name=_('teams'), related_name='partner_projects', blank=True)
    organizations = models.ManyToManyField('organization-network.Organization', verbose_name=_('organizations'), blank=True)
    website = models.URLField(_('website'), max_length=512, blank=True)
    topic = models.ForeignKey('ProjectTopic', verbose_name=_('topic'), related_name='projects', blank=True, null=True)

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _("projects")
        ordering = ['-date_from', '-date_to']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
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


class ProjectTopic(Named):

    parent = models.ForeignKey('ProjectTopic', verbose_name=_('parent topic'), related_name='topics', blank=True, null=True)

    class Meta:
        verbose_name = _('project topic')
        verbose_name_plural = _("project topics")
        ordering = ['name',]

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


class ProjectPlaylist(PlaylistRelated):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='playlists', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectLink(Link):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectImage(Image):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectFile(File):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='files', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectBlock(Block):


    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectTopicPage(Page, SubTitled):

    project_topic = models.ForeignKey('ProjectTopic', verbose_name=_('project topic'), related_name="pages", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('project topic page')
        verbose_name_plural = _("project topic pages")


class ProjectDemo(Displayable, RichText):

    project = models.ForeignKey('Project', verbose_name=_('project'), related_name='demos', blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, verbose_name=_('author'), related_name='demos', blank=True, null=True, on_delete=models.SET_NULL)
    repository = models.ForeignKey('Repository', verbose_name=_('repository'), related_name='demos', blank=True, null=True, on_delete=models.SET_NULL)
    directory = models.CharField(_('directory'), max_length=256, blank=True, null=True)
    build_commands = models.TextField(_('build commands'), blank=True)

    class Meta:
        verbose_name = _('project demo')
        verbose_name_plural = _("project demos")

    def get_absolute_url(self):
        return reverse("organization-project-demo-detail", kwargs={"slug": self.slug})

    def build(self):
        os.chdir(settings.PROJECT_DEMOS_DIR + os.sep + self.directory)
        for commands in self.build_commands.split('\n'):
            os.system(command)


class Repository(Named, URL):

    system = models.ForeignKey('RepositorySystem', verbose_name=_('system'), related_name='repositories')
    access = models.CharField(_('access'), max_length=64, choices=ACCESS_CHOICES, default='private')
    branch = models.CharField(_('branch'), max_length=32, default='master')

    class Meta:
        verbose_name = _('repository')
        verbose_name_plural = _("repositories")

    def clone(self):
        os.system(' '.join((self.system.clone_command, self.url, settings.PROJECT_DEMOS_DIR)))


class RepositorySystem(Named):

    type = models.CharField(_('type'), max_length=32)
    clone_command = models.CharField(_('clone command'), max_length=256)
    pull_command = models.CharField(_('pull command'), max_length=256)
    checkout_command = models.CharField(_('checkout command'), max_length=256)
    branch_command = models.CharField(_('branch command'), max_length=256)

    class Meta:
        verbose_name = _('repository system')
        verbose_name_plural = _("repository systems")
