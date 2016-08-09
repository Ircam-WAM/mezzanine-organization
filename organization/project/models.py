from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import RichText, Displayable, Slugged, Orderable

from organization.core.models import *
from organization.team.models import Person, Team, Organization


class Project(Displayable, RichText):
    """(Project description)"""

    leader_team = models.ForeignKey(Team, verbose_name=_('lead team'), related_name='project_leader', blank=True, null=True)
    partner_persons = models.ManyToManyField(Person, verbose_name=_('partner persons'), blank=True)
    partner_teams = models.ManyToManyField(Team, verbose_name=_('partner teams'), related_name='project_partners', blank=True)
    partner_organizations = models.ManyToManyField(Organization, verbose_name=_('partner organizations'), blank=True)
    website = models.URLField(_('website'), max_length=512, blank=True)

    class Meta:
        verbose_name = _('project')

    def __unicode__(self):
        return self.title


class ProjectBlock(Block):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectImage(Image):

    project = models.ForeignKey(Project, related_name='images')


class ProjectLink(Link):

    project = models.ForeignKey(Project, related_name='links')
