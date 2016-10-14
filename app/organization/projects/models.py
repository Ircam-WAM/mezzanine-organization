from __future__ import unicode_literals
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import RichText, Displayable, Slugged, Orderable

from organization.core.models import *
from organization.pages.models import *


PROJECT_TYPE_CHOICES = [
    ('internal', _('internal')),
    ('external', _('external')),
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
        ordering = ['name',]

    def __str__(self):
        if self.parent:
            return ' - '.join((self.parent.name, self.name))
        else:
            return self.name


class ProjectProgram(Named):

    class Meta:
        verbose_name = _('program')
        ordering = ['name',]


class ProjectProgramType(Named):

    class Meta:
        verbose_name = _('program type')
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
